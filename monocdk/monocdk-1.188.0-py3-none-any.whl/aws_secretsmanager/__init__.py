'''
# AWS Secrets Manager Construct Library

```python
import monocdk as secretsmanager
```

## Create a new Secret in a Stack

In order to have SecretsManager generate a new secret value automatically,
you can get started with the following:

```python
# Default secret
secret = secretsmanager.Secret(self, "Secret")
# Using the default secret
iam.User(self, "User",
    password=secret.secret_value
)
# Templated secret
templated_secret = secretsmanager.Secret(self, "TemplatedSecret",
    generate_secret_string=secretsmanager.aws_secretsmanager.SecretStringGenerator(
        secret_string_template=JSON.stringify({"username": "user"}),
        generate_string_key="password"
    )
)
# Using the templated secret
iam.User(self, "OtherUser",
    user_name=templated_secret.secret_value_from_json("username").to_string(),
    password=templated_secret.secret_value_from_json("password")
)
```

If you need to use a pre-existing secret, the recommended way is to manually
provision the secret in *AWS SecretsManager* and use the `Secret.fromSecretArn`
or `Secret.fromSecretAttributes` method to make it available in your CDK Application:

```python
# encryption_key: kms.Key

secret = secretsmanager.Secret.from_secret_attributes(self, "ImportedSecret",
    secret_arn="arn:aws:secretsmanager:<region>:<account-id-number>:secret:<secret-name>-<random-6-characters>",
    # If the secret is encrypted using a KMS-hosted CMK, either import or reference that key:
    encryption_key=encryption_key
)
```

SecretsManager secret values can only be used in select set of properties. For the
list of properties, see [the CloudFormation Dynamic References documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html).

A secret can set `RemovalPolicy`. If it set to `RETAIN`, that removing a secret will fail.

## Grant permission to use the secret to a role

You must grant permission to a resource for that resource to be allowed to
use a secret. This can be achieved with the `Secret.grantRead` and/or `Secret.grantWrite`
method, depending on your need:

```python
role = iam.Role(self, "SomeRole", assumed_by=iam.AccountRootPrincipal())
secret = secretsmanager.Secret(self, "Secret")
secret.grant_read(role)
secret.grant_write(role)
```

If, as in the following example, your secret was created with a KMS key:

```python
# role: iam.Role

key = kms.Key(self, "KMS")
secret = secretsmanager.Secret(self, "Secret", encryption_key=key)
secret.grant_read(role)
secret.grant_write(role)
```

then `Secret.grantRead` and `Secret.grantWrite` will also grant the role the
relevant encrypt and decrypt permissions to the KMS key through the
SecretsManager service principal.

The principal is automatically added to Secret resource policy and KMS Key policy for cross account access:

```python
other_account = iam.AccountPrincipal("1234")
key = kms.Key(self, "KMS")
secret = secretsmanager.Secret(self, "Secret", encryption_key=key)
secret.grant_read(other_account)
```

## Rotating a Secret

### Using a Custom Lambda Function

A rotation schedule can be added to a Secret using a custom Lambda function:

```python
import monocdk as lambda_

# fn: lambda.Function

secret = secretsmanager.Secret(self, "Secret")

secret.add_rotation_schedule("RotationSchedule",
    rotation_lambda=fn,
    automatically_after=Duration.days(15)
)
```

Note: The required permissions for Lambda to call SecretsManager and the other way round are automatically granted based on [AWS Documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions.html) as long as the Lambda is not imported.

See [Overview of the Lambda Rotation Function](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-lambda-function-overview.html) on how to implement a Lambda Rotation Function.

### Using a Hosted Lambda Function

Use the `hostedRotation` prop to rotate a secret with a hosted Lambda function:

```python
secret = secretsmanager.Secret(self, "Secret")

secret.add_rotation_schedule("RotationSchedule",
    hosted_rotation=secretsmanager.HostedRotation.mysql_single_user()
)
```

Hosted rotation is available for secrets representing credentials for MySQL, PostgreSQL, Oracle,
MariaDB, SQLServer, Redshift and MongoDB (both for the single and multi user schemes).

When deployed in a VPC, the hosted rotation implements `ec2.IConnectable`:

```python
# my_vpc: ec2.Vpc
# db_connections: ec2.Connections
# secret: secretsmanager.Secret


my_hosted_rotation = secretsmanager.HostedRotation.mysql_single_user(vpc=my_vpc)
secret.add_rotation_schedule("RotationSchedule", hosted_rotation=my_hosted_rotation)
db_connections.allow_default_port_from(my_hosted_rotation)
```

See also [Automating secret creation in AWS CloudFormation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_cloudformation.html).

## Rotating database credentials

Define a `SecretRotation` to rotate database credentials:

```python
# my_secret: secretsmanager.Secret
# my_database: ec2.IConnectable
# my_vpc: ec2.Vpc


secretsmanager.SecretRotation(self, "SecretRotation",
    application=secretsmanager.SecretRotationApplication.MYSQL_ROTATION_SINGLE_USER,  # MySQL single user scheme
    secret=my_secret,
    target=my_database,  # a Connectable
    vpc=my_vpc,  # The VPC where the secret rotation application will be deployed
    exclude_characters=" %+:;{}"
)
```

The secret must be a JSON string with the following format:

```json
{
  "engine": "<required: database engine>",
  "host": "<required: instance host name>",
  "username": "<required: username>",
  "password": "<required: password>",
  "dbname": "<optional: database name>",
  "port": "<optional: if not specified, default port will be used>",
  "masterarn": "<required for multi user rotation: the arn of the master secret which will be used to create users/change passwords>"
}
```

For the multi user scheme, a `masterSecret` must be specified:

```python
# my_user_secret: secretsmanager.Secret
# my_master_secret: secretsmanager.Secret
# my_database: ec2.IConnectable
# my_vpc: ec2.Vpc


secretsmanager.SecretRotation(self, "SecretRotation",
    application=secretsmanager.SecretRotationApplication.MYSQL_ROTATION_MULTI_USER,
    secret=my_user_secret,  # The secret that will be rotated
    master_secret=my_master_secret,  # The secret used for the rotation
    target=my_database,
    vpc=my_vpc
)
```

See also [aws-rds](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-rds/README.md) where
credentials generation and rotation is integrated.

## Importing Secrets

Existing secrets can be imported by ARN, name, and other attributes (including the KMS key used to encrypt the secret).
Secrets imported by name should use the short-form of the name (without the SecretsManager-provided suffx);
the secret name must exist in the same account and region as the stack.
Importing by name makes it easier to reference secrets created in different regions, each with their own suffix and ARN.

```python
secret_complete_arn = "arn:aws:secretsmanager:eu-west-1:111111111111:secret:MySecret-f3gDy9"
secret_partial_arn = "arn:aws:secretsmanager:eu-west-1:111111111111:secret:MySecret" # No Secrets Manager suffix
encryption_key = kms.Key.from_key_arn(self, "MyEncKey", "arn:aws:kms:eu-west-1:111111111111:key/21c4b39b-fde2-4273-9ac0-d9bb5c0d0030")
my_secret_from_complete_arn = secretsmanager.Secret.from_secret_complete_arn(self, "SecretFromCompleteArn", secret_complete_arn)
my_secret_from_partial_arn = secretsmanager.Secret.from_secret_partial_arn(self, "SecretFromPartialArn", secret_partial_arn)
my_secret_from_name = secretsmanager.Secret.from_secret_name_v2(self, "SecretFromName", "MySecret")
my_secret_from_attrs = secretsmanager.Secret.from_secret_attributes(self, "SecretFromAttributes",
    secret_complete_arn=secret_complete_arn,
    encryption_key=encryption_key
)
```

## Replicating secrets

Secrets can be replicated to multiple regions by specifying `replicaRegions`:

```python
# my_key: kms.Key

secretsmanager.Secret(self, "Secret",
    replica_regions=[secretsmanager.aws_secretsmanager.ReplicaRegion(
        region="eu-west-1"
    ), secretsmanager.aws_secretsmanager.ReplicaRegion(
        region="eu-central-1",
        encryption_key=my_key
    )
    ]
)
```

Alternatively, use `addReplicaRegion()`:

```python
secret = secretsmanager.Secret(self, "Secret")
secret.add_replica_region("eu-west-1")
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
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_ec2 import (
    Connections as _Connections_57ccbda9,
    IConnectable as _IConnectable_c1c0e72c,
    IInterfaceVpcEndpoint as _IInterfaceVpcEndpoint_6081623d,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import (
    AddToResourcePolicyResult as _AddToResourcePolicyResult_0fd9d2a9,
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    PolicyDocument as _PolicyDocument_b5de5177,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_lambda import IFunction as _IFunction_6e14f09e


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.AttachedSecretOptions",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class AttachedSecretOptions:
    def __init__(self, *, target: "ISecretAttachmentTarget") -> None:
        '''(experimental) Options to add a secret attachment to a secret.

        :param target: (experimental) The target to attach the secret to.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            # secret_attachment_target: secretsmanager.ISecretAttachmentTarget
            
            attached_secret_options = secretsmanager.AttachedSecretOptions(
                target=secret_attachment_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc9e7a1d3cbbf406c3cf36e9155ecf967fd10750a8fea967ea8ffab53e86565)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }

    @builtins.property
    def target(self) -> "ISecretAttachmentTarget":
        '''(experimental) The target to attach the secret to.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("ISecretAttachmentTarget", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachedSecretOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_secretsmanager.AttachmentTargetType")
class AttachmentTargetType(enum.Enum):
    '''(experimental) The type of service or database that's being associated with the secret.

    :stability: experimental
    '''

    INSTANCE = "INSTANCE"
    '''(deprecated) A database instance.

    :deprecated: use RDS_DB_INSTANCE instead

    :stability: deprecated
    '''
    CLUSTER = "CLUSTER"
    '''(deprecated) A database cluster.

    :deprecated: use RDS_DB_CLUSTER instead

    :stability: deprecated
    '''
    RDS_DB_INSTANCE = "RDS_DB_INSTANCE"
    '''(experimental) AWS::RDS::DBInstance.

    :stability: experimental
    '''
    RDS_DB_CLUSTER = "RDS_DB_CLUSTER"
    '''(experimental) AWS::RDS::DBCluster.

    :stability: experimental
    '''
    RDS_DB_PROXY = "RDS_DB_PROXY"
    '''(experimental) AWS::RDS::DBProxy.

    :stability: experimental
    '''
    REDSHIFT_CLUSTER = "REDSHIFT_CLUSTER"
    '''(experimental) AWS::Redshift::Cluster.

    :stability: experimental
    '''
    DOCDB_DB_INSTANCE = "DOCDB_DB_INSTANCE"
    '''(experimental) AWS::DocDB::DBInstance.

    :stability: experimental
    '''
    DOCDB_DB_CLUSTER = "DOCDB_DB_CLUSTER"
    '''(experimental) AWS::DocDB::DBCluster.

    :stability: experimental
    '''


@jsii.implements(_IInspectable_82c04a63)
class CfnResourcePolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.CfnResourcePolicy",
):
    '''A CloudFormation ``AWS::SecretsManager::ResourcePolicy``.

    Attaches a resource-based permission policy to a secret. A resource-based policy is optional. For more information, see `Authentication and access control for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html>`_

    For information about attaching a policy in the console, see `Attach a permissions policy to a secret <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_resource-based-policies.html>`_ .

    *Required permissions:* ``secretsmanager:PutResourcePolicy`` . For more information, see `IAM policy actions for Secrets Manager <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssecretsmanager.html#awssecretsmanager-actions-as-permissions>`_ and `Authentication and access control in Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html>`_ .

    :cloudformationResource: AWS::SecretsManager::ResourcePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_secretsmanager as secretsmanager
        
        # resource_policy: Any
        
        cfn_resource_policy = secretsmanager.CfnResourcePolicy(self, "MyCfnResourcePolicy",
            resource_policy=resource_policy,
            secret_id="secretId",
        
            # the properties below are optional
            block_public_policy=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resource_policy: typing.Any,
        secret_id: builtins.str,
        block_public_policy: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::SecretsManager::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_policy: A JSON-formatted string for an AWS resource-based policy. For example policies, see `Permissions policy examples <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html>`_ .
        :param secret_id: The ARN or name of the secret to attach the resource-based policy. For an ARN, we recommend that you specify a complete ARN rather than a partial ARN.
        :param block_public_policy: Specifies whether to block resource-based policies that allow broad access to the secret. By default, Secrets Manager blocks policies that allow broad access, for example those that use a wildcard for the principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e150ea28ef4b0f25a0eef706af436d1e3482033b921cb723167aa8f6b1d75739)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourcePolicyProps(
            resource_policy=resource_policy,
            secret_id=secret_id,
            block_public_policy=block_public_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea43da867688023566a0be83c5f82c9691b0ad05ec09a14692965ccd667984e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcd41eee94e0284d231384addb9acfa7724515d1eb5d445c7bc70036fbd77c39)
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
    @jsii.member(jsii_name="resourcePolicy")
    def resource_policy(self) -> typing.Any:
        '''A JSON-formatted string for an AWS resource-based policy.

        For example policies, see `Permissions policy examples <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "resourcePolicy"))

    @resource_policy.setter
    def resource_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc990d92d95299d84354eb546c8320628b7b8328ec3314bbe11662e7360adcef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        '''The ARN or name of the secret to attach the resource-based policy.

        For an ARN, we recommend that you specify a complete ARN rather than a partial ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c0c2613fd8951e4f86ce669e1bc45b3b79d015edc0fa6e926544dd75e682ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value)

    @builtins.property
    @jsii.member(jsii_name="blockPublicPolicy")
    def block_public_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to block resource-based policies that allow broad access to the secret.

        By default, Secrets Manager blocks policies that allow broad access, for example those that use a wildcard for the principal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-blockpublicpolicy
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "blockPublicPolicy"))

    @block_public_policy.setter
    def block_public_policy(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf5214200e72ff19db4afea8dc3e9bf2b9b199dca5b196fb7ca8d76d1bfea79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockPublicPolicy", value)


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_policy": "resourcePolicy",
        "secret_id": "secretId",
        "block_public_policy": "blockPublicPolicy",
    },
)
class CfnResourcePolicyProps:
    def __init__(
        self,
        *,
        resource_policy: typing.Any,
        secret_id: builtins.str,
        block_public_policy: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourcePolicy``.

        :param resource_policy: A JSON-formatted string for an AWS resource-based policy. For example policies, see `Permissions policy examples <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html>`_ .
        :param secret_id: The ARN or name of the secret to attach the resource-based policy. For an ARN, we recommend that you specify a complete ARN rather than a partial ARN.
        :param block_public_policy: Specifies whether to block resource-based policies that allow broad access to the secret. By default, Secrets Manager blocks policies that allow broad access, for example those that use a wildcard for the principal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            # resource_policy: Any
            
            cfn_resource_policy_props = secretsmanager.CfnResourcePolicyProps(
                resource_policy=resource_policy,
                secret_id="secretId",
            
                # the properties below are optional
                block_public_policy=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f2a968037f043ebc0e399ed715cb98a161407eee89ad77829aa8e9abaefca5)
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument block_public_policy", value=block_public_policy, expected_type=type_hints["block_public_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_policy": resource_policy,
            "secret_id": secret_id,
        }
        if block_public_policy is not None:
            self._values["block_public_policy"] = block_public_policy

    @builtins.property
    def resource_policy(self) -> typing.Any:
        '''A JSON-formatted string for an AWS resource-based policy.

        For example policies, see `Permissions policy examples <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        '''
        result = self._values.get("resource_policy")
        assert result is not None, "Required property 'resource_policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''The ARN or name of the secret to attach the resource-based policy.

        For an ARN, we recommend that you specify a complete ARN rather than a partial ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def block_public_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to block resource-based policies that allow broad access to the secret.

        By default, Secrets Manager blocks policies that allow broad access, for example those that use a wildcard for the principal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-blockpublicpolicy
        '''
        result = self._values.get("block_public_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRotationSchedule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.CfnRotationSchedule",
):
    '''A CloudFormation ``AWS::SecretsManager::RotationSchedule``.

    Sets the rotation schedule and Lambda rotation function for a secret. For more information, see `How rotation works <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ . For the rotation function, you have two options:

    - You can create a new rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ by using ``HostedRotationLambda`` .
    - You can choose an existing rotation function by using ``RotationLambdaARN`` .

    For Amazon RDS , Amazon Redshift , Amazon DocumentDB secrets, if you define both the secret and the database or service in the AWS CloudFormation template, then you need to define the `AWS::SecretsManager::SecretTargetAttachment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html>`_ resource to populate the secret with the connection details of the database or service before you attempt to configure rotation.

    :cloudformationResource: AWS::SecretsManager::RotationSchedule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_secretsmanager as secretsmanager
        
        cfn_rotation_schedule = secretsmanager.CfnRotationSchedule(self, "MyCfnRotationSchedule",
            secret_id="secretId",
        
            # the properties below are optional
            hosted_rotation_lambda=secretsmanager.CfnRotationSchedule.HostedRotationLambdaProperty(
                rotation_type="rotationType",
        
                # the properties below are optional
                exclude_characters="excludeCharacters",
                kms_key_arn="kmsKeyArn",
                master_secret_arn="masterSecretArn",
                master_secret_kms_key_arn="masterSecretKmsKeyArn",
                rotation_lambda_name="rotationLambdaName",
                superuser_secret_arn="superuserSecretArn",
                superuser_secret_kms_key_arn="superuserSecretKmsKeyArn",
                vpc_security_group_ids="vpcSecurityGroupIds",
                vpc_subnet_ids="vpcSubnetIds"
            ),
            rotate_immediately_on_update=False,
            rotation_lambda_arn="rotationLambdaArn",
            rotation_rules=secretsmanager.CfnRotationSchedule.RotationRulesProperty(
                automatically_after_days=123,
                duration="duration",
                schedule_expression="scheduleExpression"
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        secret_id: builtins.str,
        hosted_rotation_lambda: typing.Optional[typing.Union[typing.Union["CfnRotationSchedule.HostedRotationLambdaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        rotate_immediately_on_update: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        rotation_lambda_arn: typing.Optional[builtins.str] = None,
        rotation_rules: typing.Optional[typing.Union[typing.Union["CfnRotationSchedule.RotationRulesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::SecretsManager::RotationSchedule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param secret_id: The ARN or name of the secret to rotate. To reference a secret also created in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.
        :param hosted_rotation_lambda: Creates a new Lambda rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ . To use a rotation function that already exists, specify ``RotationLambdaARN`` instead.
        :param rotate_immediately_on_update: Specifies whether to rotate the secret immediately or wait until the next scheduled rotation window. The rotation schedule is defined in ``RotationRules`` . If you don't immediately rotate the secret, Secrets Manager tests the rotation configuration by running the ```testSecret`` step <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ of the Lambda rotation function. The test creates an ``AWSPENDING`` version of the secret and then removes it. If you don't specify this value, then by default, Secrets Manager rotates the secret immediately. Rotation is an asynchronous process. For more information, see `How rotation works <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ .
        :param rotation_lambda_arn: The ARN of an existing Lambda rotation function. To specify a rotation function that is also defined in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function. To create a new rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ , specify ``HostedRotationLambda`` instead.
        :param rotation_rules: A structure that defines the rotation configuration for this secret.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b05e81d2584648f9ee8606b4d8692ac1107eff30872855d7c6cb3cbbcfa10a1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRotationScheduleProps(
            secret_id=secret_id,
            hosted_rotation_lambda=hosted_rotation_lambda,
            rotate_immediately_on_update=rotate_immediately_on_update,
            rotation_lambda_arn=rotation_lambda_arn,
            rotation_rules=rotation_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f638a0ec15bde8dc2b468d1c204a08641561580102589c8e8cbfbee892a51a6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa44e940b824df54ce4a81fb1a84e098cf7c77005251371ac915f11accd6a065)
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
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        '''The ARN or name of the secret to rotate.

        To reference a secret also created in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f370d4c3ad544299de955b56a01d31094df5799510865b65bbd972ddec42f4a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value)

    @builtins.property
    @jsii.member(jsii_name="hostedRotationLambda")
    def hosted_rotation_lambda(
        self,
    ) -> typing.Optional[typing.Union["CfnRotationSchedule.HostedRotationLambdaProperty", _IResolvable_a771d0ef]]:
        '''Creates a new Lambda rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ . To use a rotation function that already exists, specify ``RotationLambdaARN`` instead.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda
        '''
        return typing.cast(typing.Optional[typing.Union["CfnRotationSchedule.HostedRotationLambdaProperty", _IResolvable_a771d0ef]], jsii.get(self, "hostedRotationLambda"))

    @hosted_rotation_lambda.setter
    def hosted_rotation_lambda(
        self,
        value: typing.Optional[typing.Union["CfnRotationSchedule.HostedRotationLambdaProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5674db8b9f3df6c9bffa8fbeb215204b32874e4cbf3cacac2e883aba54b563b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostedRotationLambda", value)

    @builtins.property
    @jsii.member(jsii_name="rotateImmediatelyOnUpdate")
    def rotate_immediately_on_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to rotate the secret immediately or wait until the next scheduled rotation window.

        The rotation schedule is defined in ``RotationRules`` .

        If you don't immediately rotate the secret, Secrets Manager tests the rotation configuration by running the ```testSecret`` step <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ of the Lambda rotation function. The test creates an ``AWSPENDING`` version of the secret and then removes it.

        If you don't specify this value, then by default, Secrets Manager rotates the secret immediately.

        Rotation is an asynchronous process. For more information, see `How rotation works <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotateimmediatelyonupdate
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "rotateImmediatelyOnUpdate"))

    @rotate_immediately_on_update.setter
    def rotate_immediately_on_update(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44719747806e5a20dfa5bc090319856defe011e532d9a35e0d971d81520fcbc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotateImmediatelyOnUpdate", value)

    @builtins.property
    @jsii.member(jsii_name="rotationLambdaArn")
    def rotation_lambda_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an existing Lambda rotation function.

        To specify a rotation function that is also defined in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function.

        To create a new rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ , specify ``HostedRotationLambda`` instead.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationLambdaArn"))

    @rotation_lambda_arn.setter
    def rotation_lambda_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3edecee3376a880267fe46d4314bcda32e33f70e64000766bcf36ee0ba32a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationLambdaArn", value)

    @builtins.property
    @jsii.member(jsii_name="rotationRules")
    def rotation_rules(
        self,
    ) -> typing.Optional[typing.Union["CfnRotationSchedule.RotationRulesProperty", _IResolvable_a771d0ef]]:
        '''A structure that defines the rotation configuration for this secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        '''
        return typing.cast(typing.Optional[typing.Union["CfnRotationSchedule.RotationRulesProperty", _IResolvable_a771d0ef]], jsii.get(self, "rotationRules"))

    @rotation_rules.setter
    def rotation_rules(
        self,
        value: typing.Optional[typing.Union["CfnRotationSchedule.RotationRulesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6cdc07df79420ebc4b70d2c20585eb33118bb7f876f8bed5e9f7902ba35a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationRules", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_secretsmanager.CfnRotationSchedule.HostedRotationLambdaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rotation_type": "rotationType",
            "exclude_characters": "excludeCharacters",
            "kms_key_arn": "kmsKeyArn",
            "master_secret_arn": "masterSecretArn",
            "master_secret_kms_key_arn": "masterSecretKmsKeyArn",
            "rotation_lambda_name": "rotationLambdaName",
            "superuser_secret_arn": "superuserSecretArn",
            "superuser_secret_kms_key_arn": "superuserSecretKmsKeyArn",
            "vpc_security_group_ids": "vpcSecurityGroupIds",
            "vpc_subnet_ids": "vpcSubnetIds",
        },
    )
    class HostedRotationLambdaProperty:
        def __init__(
            self,
            *,
            rotation_type: builtins.str,
            exclude_characters: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
            master_secret_arn: typing.Optional[builtins.str] = None,
            master_secret_kms_key_arn: typing.Optional[builtins.str] = None,
            rotation_lambda_name: typing.Optional[builtins.str] = None,
            superuser_secret_arn: typing.Optional[builtins.str] = None,
            superuser_secret_kms_key_arn: typing.Optional[builtins.str] = None,
            vpc_security_group_ids: typing.Optional[builtins.str] = None,
            vpc_subnet_ids: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Creates a new Lambda rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ .

            You must specify ``Transform: AWS::SecretsManager-2020-07-23`` at the beginning of the CloudFormation template.

            :param rotation_type: The rotation template to base the rotation function on, one of the following:. - ``MySQLSingleUser`` to use the template `SecretsManagerRDSMySQLRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mysql-singleuser>`_ . - ``MySQLMultiUser`` to use the template `SecretsManagerRDSMySQLRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mysql-multiuser>`_ . - ``PostgreSQLSingleUser`` to use the template `SecretsManagerRDSPostgreSQLRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-postgre-singleuser>`_ - ``PostgreSQLMultiUser`` to use the template `SecretsManagerRDSPostgreSQLRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-postgre-multiuser>`_ . - ``OracleSingleUser`` to use the template `SecretsManagerRDSOracleRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-oracle-singleuser>`_ . - ``OracleMultiUser`` to use the template `SecretsManagerRDSOracleRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-oracle-multiuser>`_ . - ``MariaDBSingleUser`` to use the template `SecretsManagerRDSMariaDBRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mariadb-singleuser>`_ . - ``MariaDBMultiUser`` to use the template `SecretsManagerRDSMariaDBRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mariadb-multiuser>`_ . - ``SQLServerSingleUser`` to use the template `SecretsManagerRDSSQLServerRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-sqlserver-singleuser>`_ . - ``SQLServerMultiUser`` to use the template `SecretsManagerRDSSQLServerRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-sqlserver-multiuser>`_ . - ``RedshiftSingleUser`` to use the template `SecretsManagerRedshiftRotationSingleUsr <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-redshift-singleuser>`_ . - ``RedshiftMultiUser`` to use the template `SecretsManagerRedshiftRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-redshift-multiuser>`_ . - ``MongoDBSingleUser`` to use the template `SecretsManagerMongoDBRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mongodb-singleuser>`_ . - ``MongoDBMultiUser`` to use the template `SecretsManagerMongoDBRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mongodb-multiuser>`_ .
            :param exclude_characters: A string of the characters that you don't want in the password.
            :param kms_key_arn: The ARN of the KMS key that Secrets Manager uses to encrypt the secret. If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If ``aws/secretsmanager`` doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.
            :param master_secret_arn: The ARN of the secret that contains elevated credentials. You must create the elevated secret before you can set this property. The Lambda rotation function uses this secret for the `Alternating users rotation strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . You can specify ``MasterSecretArn`` or ``SuperuserSecretArn`` but not both. They represent the same superuser secret.
            :param master_secret_kms_key_arn: The ARN of the KMS key that Secrets Manager uses to encrypt the elevated secret if you use the `alternating users strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . If you don't specify this value and you use the alternating users strategy, then Secrets Manager uses the key ``aws/secretsmanager`` . If ``aws/secretsmanager`` doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value. You can specify ``MasterSecretKmsKeyArn`` or ``SuperuserSecretKmsKeyArn`` but not both. They represent the same superuser secret KMS key .
            :param rotation_lambda_name: The name of the Lambda rotation function.
            :param superuser_secret_arn: The ARN of the secret that contains elevated credentials. You must create the superuser secret before you can set this property. The Lambda rotation function uses this secret for the `Alternating users rotation strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . You can specify ``MasterSecretArn`` or ``SuperuserSecretArn`` but not both. They represent the same superuser secret.
            :param superuser_secret_kms_key_arn: The ARN of the KMS key that Secrets Manager uses to encrypt the elevated secret if you use the `alternating users strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . If you don't specify this value and you use the alternating users strategy, then Secrets Manager uses the key ``aws/secretsmanager`` . If ``aws/secretsmanager`` doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value. You can specify ``MasterSecretKmsKeyArn`` or ``SuperuserSecretKmsKeyArn`` but not both. They represent the same superuser secret KMS key .
            :param vpc_security_group_ids: A comma-separated list of security group IDs applied to the target database. The templates applies the same security groups as on the Lambda rotation function that is created as part of this stack.
            :param vpc_subnet_ids: A comma separated list of VPC subnet IDs of the target database network. The Lambda rotation function is in the same subnet group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_secretsmanager as secretsmanager
                
                hosted_rotation_lambda_property = secretsmanager.CfnRotationSchedule.HostedRotationLambdaProperty(
                    rotation_type="rotationType",
                
                    # the properties below are optional
                    exclude_characters="excludeCharacters",
                    kms_key_arn="kmsKeyArn",
                    master_secret_arn="masterSecretArn",
                    master_secret_kms_key_arn="masterSecretKmsKeyArn",
                    rotation_lambda_name="rotationLambdaName",
                    superuser_secret_arn="superuserSecretArn",
                    superuser_secret_kms_key_arn="superuserSecretKmsKeyArn",
                    vpc_security_group_ids="vpcSecurityGroupIds",
                    vpc_subnet_ids="vpcSubnetIds"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d21cca99480caf5adc27fdc5bbf0f89705819515be41087372db6f9b977b8044)
                check_type(argname="argument rotation_type", value=rotation_type, expected_type=type_hints["rotation_type"])
                check_type(argname="argument exclude_characters", value=exclude_characters, expected_type=type_hints["exclude_characters"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument master_secret_arn", value=master_secret_arn, expected_type=type_hints["master_secret_arn"])
                check_type(argname="argument master_secret_kms_key_arn", value=master_secret_kms_key_arn, expected_type=type_hints["master_secret_kms_key_arn"])
                check_type(argname="argument rotation_lambda_name", value=rotation_lambda_name, expected_type=type_hints["rotation_lambda_name"])
                check_type(argname="argument superuser_secret_arn", value=superuser_secret_arn, expected_type=type_hints["superuser_secret_arn"])
                check_type(argname="argument superuser_secret_kms_key_arn", value=superuser_secret_kms_key_arn, expected_type=type_hints["superuser_secret_kms_key_arn"])
                check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
                check_type(argname="argument vpc_subnet_ids", value=vpc_subnet_ids, expected_type=type_hints["vpc_subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rotation_type": rotation_type,
            }
            if exclude_characters is not None:
                self._values["exclude_characters"] = exclude_characters
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if master_secret_arn is not None:
                self._values["master_secret_arn"] = master_secret_arn
            if master_secret_kms_key_arn is not None:
                self._values["master_secret_kms_key_arn"] = master_secret_kms_key_arn
            if rotation_lambda_name is not None:
                self._values["rotation_lambda_name"] = rotation_lambda_name
            if superuser_secret_arn is not None:
                self._values["superuser_secret_arn"] = superuser_secret_arn
            if superuser_secret_kms_key_arn is not None:
                self._values["superuser_secret_kms_key_arn"] = superuser_secret_kms_key_arn
            if vpc_security_group_ids is not None:
                self._values["vpc_security_group_ids"] = vpc_security_group_ids
            if vpc_subnet_ids is not None:
                self._values["vpc_subnet_ids"] = vpc_subnet_ids

        @builtins.property
        def rotation_type(self) -> builtins.str:
            '''The rotation template to base the rotation function on, one of the following:.

            - ``MySQLSingleUser`` to use the template `SecretsManagerRDSMySQLRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mysql-singleuser>`_ .
            - ``MySQLMultiUser`` to use the template `SecretsManagerRDSMySQLRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mysql-multiuser>`_ .
            - ``PostgreSQLSingleUser`` to use the template `SecretsManagerRDSPostgreSQLRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-postgre-singleuser>`_
            - ``PostgreSQLMultiUser`` to use the template `SecretsManagerRDSPostgreSQLRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-postgre-multiuser>`_ .
            - ``OracleSingleUser`` to use the template `SecretsManagerRDSOracleRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-oracle-singleuser>`_ .
            - ``OracleMultiUser`` to use the template `SecretsManagerRDSOracleRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-oracle-multiuser>`_ .
            - ``MariaDBSingleUser`` to use the template `SecretsManagerRDSMariaDBRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mariadb-singleuser>`_ .
            - ``MariaDBMultiUser`` to use the template `SecretsManagerRDSMariaDBRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mariadb-multiuser>`_ .
            - ``SQLServerSingleUser`` to use the template `SecretsManagerRDSSQLServerRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-sqlserver-singleuser>`_ .
            - ``SQLServerMultiUser`` to use the template `SecretsManagerRDSSQLServerRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-sqlserver-multiuser>`_ .
            - ``RedshiftSingleUser`` to use the template `SecretsManagerRedshiftRotationSingleUsr <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-redshift-singleuser>`_ .
            - ``RedshiftMultiUser`` to use the template `SecretsManagerRedshiftRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-redshift-multiuser>`_ .
            - ``MongoDBSingleUser`` to use the template `SecretsManagerMongoDBRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mongodb-singleuser>`_ .
            - ``MongoDBMultiUser`` to use the template `SecretsManagerMongoDBRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mongodb-multiuser>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-rotationtype
            '''
            result = self._values.get("rotation_type")
            assert result is not None, "Required property 'rotation_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def exclude_characters(self) -> typing.Optional[builtins.str]:
            '''A string of the characters that you don't want in the password.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-excludecharacters
            '''
            result = self._values.get("exclude_characters")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key that Secrets Manager uses to encrypt the secret.

            If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If ``aws/secretsmanager`` doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that contains elevated credentials.

            You must create the elevated secret before you can set this property. The Lambda rotation function uses this secret for the `Alternating users rotation strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ .

            You can specify ``MasterSecretArn`` or ``SuperuserSecretArn`` but not both. They represent the same superuser secret.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-mastersecretarn
            '''
            result = self._values.get("master_secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_secret_kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key that Secrets Manager uses to encrypt the elevated secret if you use the `alternating users strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . If you don't specify this value and you use the alternating users strategy, then Secrets Manager uses the key ``aws/secretsmanager`` . If ``aws/secretsmanager`` doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.

            You can specify ``MasterSecretKmsKeyArn`` or ``SuperuserSecretKmsKeyArn`` but not both. They represent the same superuser secret KMS key .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-mastersecretkmskeyarn
            '''
            result = self._values.get("master_secret_kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rotation_lambda_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Lambda rotation function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-rotationlambdaname
            '''
            result = self._values.get("rotation_lambda_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def superuser_secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that contains elevated credentials.

            You must create the superuser secret before you can set this property. The Lambda rotation function uses this secret for the `Alternating users rotation strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ .

            You can specify ``MasterSecretArn`` or ``SuperuserSecretArn`` but not both. They represent the same superuser secret.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-superusersecretarn
            '''
            result = self._values.get("superuser_secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def superuser_secret_kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key that Secrets Manager uses to encrypt the elevated secret if you use the `alternating users strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . If you don't specify this value and you use the alternating users strategy, then Secrets Manager uses the key ``aws/secretsmanager`` . If ``aws/secretsmanager`` doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.

            You can specify ``MasterSecretKmsKeyArn`` or ``SuperuserSecretKmsKeyArn`` but not both. They represent the same superuser secret KMS key .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-superusersecretkmskeyarn
            '''
            result = self._values.get("superuser_secret_kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_security_group_ids(self) -> typing.Optional[builtins.str]:
            '''A comma-separated list of security group IDs applied to the target database.

            The templates applies the same security groups as on the Lambda rotation function that is created as part of this stack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-vpcsecuritygroupids
            '''
            result = self._values.get("vpc_security_group_ids")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_subnet_ids(self) -> typing.Optional[builtins.str]:
            '''A comma separated list of VPC subnet IDs of the target database network.

            The Lambda rotation function is in the same subnet group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-vpcsubnetids
            '''
            result = self._values.get("vpc_subnet_ids")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostedRotationLambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_secretsmanager.CfnRotationSchedule.RotationRulesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automatically_after_days": "automaticallyAfterDays",
            "duration": "duration",
            "schedule_expression": "scheduleExpression",
        },
    )
    class RotationRulesProperty:
        def __init__(
            self,
            *,
            automatically_after_days: typing.Optional[jsii.Number] = None,
            duration: typing.Optional[builtins.str] = None,
            schedule_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The rotation schedule and window.

            We recommend you use ``ScheduleExpression`` to set a cron or rate expression for the schedule and ``Duration`` to set the length of the rotation window.

            :param automatically_after_days: The number of days between automatic scheduled rotations of the secret. You can use this value to check that your secret meets your compliance guidelines for how often secrets must be rotated. In ``DescribeSecret`` and ``ListSecrets`` , this value is calculated from the rotation schedule after every successful rotation. In ``RotateSecret`` , you can set the rotation schedule in ``RotationRules`` with ``AutomaticallyAfterDays`` or ``ScheduleExpression`` , but not both.
            :param duration: The length of the rotation window in hours, for example ``3h`` for a three hour window. Secrets Manager rotates your secret at any time during this window. The window must not extend into the next rotation window or the next UTC day. The window starts according to the ``ScheduleExpression`` . If you don't specify a ``Duration`` , for a ``ScheduleExpression`` in hours, the window automatically closes after one hour. For a ``ScheduleExpression`` in days, the window automatically closes at the end of the UTC day. For more information, including examples, see `Schedule expressions in Secrets Manager rotation <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html>`_ in the *Secrets Manager Users Guide* .
            :param schedule_expression: A ``cron()`` or ``rate()`` expression that defines the schedule for rotating your secret. Secrets Manager rotation schedules use UTC time zone. Secrets Manager rotates your secret any time during a rotation window. Secrets Manager ``rate()`` expressions represent the interval in hours or days that you want to rotate your secret, for example ``rate(12 hours)`` or ``rate(10 days)`` . You can rotate a secret as often as every four hours. If you use a ``rate()`` expression, the rotation window starts at midnight. For a rate in hours, the default rotation window closes after one hour. For a rate in days, the default rotation window closes at the end of the day. You can set the ``Duration`` to change the rotation window. The rotation window must not extend into the next UTC day or into the next rotation window. You can use a ``cron()`` expression to create a rotation schedule that is more detailed than a rotation interval. For more information, including examples, see `Schedule expressions in Secrets Manager rotation <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html>`_ in the *Secrets Manager Users Guide* . For a cron expression that represents a schedule in hours, the default rotation window closes after one hour. For a cron expression that represents a schedule in days, the default rotation window closes at the end of the day. You can set the ``Duration`` to change the rotation window. The rotation window must not extend into the next UTC day or into the next rotation window.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_secretsmanager as secretsmanager
                
                rotation_rules_property = secretsmanager.CfnRotationSchedule.RotationRulesProperty(
                    automatically_after_days=123,
                    duration="duration",
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af032eee28276438badaf1898ba41bce18eb796ae654f2d7239b5397f96e4ca7)
                check_type(argname="argument automatically_after_days", value=automatically_after_days, expected_type=type_hints["automatically_after_days"])
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatically_after_days is not None:
                self._values["automatically_after_days"] = automatically_after_days
            if duration is not None:
                self._values["duration"] = duration
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression

        @builtins.property
        def automatically_after_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days between automatic scheduled rotations of the secret.

            You can use this value to check that your secret meets your compliance guidelines for how often secrets must be rotated.

            In ``DescribeSecret`` and ``ListSecrets`` , this value is calculated from the rotation schedule after every successful rotation. In ``RotateSecret`` , you can set the rotation schedule in ``RotationRules`` with ``AutomaticallyAfterDays`` or ``ScheduleExpression`` , but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-automaticallyafterdays
            '''
            result = self._values.get("automatically_after_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def duration(self) -> typing.Optional[builtins.str]:
            '''The length of the rotation window in hours, for example ``3h`` for a three hour window.

            Secrets Manager rotates your secret at any time during this window. The window must not extend into the next rotation window or the next UTC day. The window starts according to the ``ScheduleExpression`` . If you don't specify a ``Duration`` , for a ``ScheduleExpression`` in hours, the window automatically closes after one hour. For a ``ScheduleExpression`` in days, the window automatically closes at the end of the UTC day. For more information, including examples, see `Schedule expressions in Secrets Manager rotation <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html>`_ in the *Secrets Manager Users Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-duration
            '''
            result = self._values.get("duration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''A ``cron()`` or ``rate()`` expression that defines the schedule for rotating your secret.

            Secrets Manager rotation schedules use UTC time zone. Secrets Manager rotates your secret any time during a rotation window.

            Secrets Manager ``rate()`` expressions represent the interval in hours or days that you want to rotate your secret, for example ``rate(12 hours)`` or ``rate(10 days)`` . You can rotate a secret as often as every four hours. If you use a ``rate()`` expression, the rotation window starts at midnight. For a rate in hours, the default rotation window closes after one hour. For a rate in days, the default rotation window closes at the end of the day. You can set the ``Duration`` to change the rotation window. The rotation window must not extend into the next UTC day or into the next rotation window.

            You can use a ``cron()`` expression to create a rotation schedule that is more detailed than a rotation interval. For more information, including examples, see `Schedule expressions in Secrets Manager rotation <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html>`_ in the *Secrets Manager Users Guide* . For a cron expression that represents a schedule in hours, the default rotation window closes after one hour. For a cron expression that represents a schedule in days, the default rotation window closes at the end of the day. You can set the ``Duration`` to change the rotation window. The rotation window must not extend into the next UTC day or into the next rotation window.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RotationRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.CfnRotationScheduleProps",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "hosted_rotation_lambda": "hostedRotationLambda",
        "rotate_immediately_on_update": "rotateImmediatelyOnUpdate",
        "rotation_lambda_arn": "rotationLambdaArn",
        "rotation_rules": "rotationRules",
    },
)
class CfnRotationScheduleProps:
    def __init__(
        self,
        *,
        secret_id: builtins.str,
        hosted_rotation_lambda: typing.Optional[typing.Union[typing.Union[CfnRotationSchedule.HostedRotationLambdaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        rotate_immediately_on_update: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        rotation_lambda_arn: typing.Optional[builtins.str] = None,
        rotation_rules: typing.Optional[typing.Union[typing.Union[CfnRotationSchedule.RotationRulesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRotationSchedule``.

        :param secret_id: The ARN or name of the secret to rotate. To reference a secret also created in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.
        :param hosted_rotation_lambda: Creates a new Lambda rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ . To use a rotation function that already exists, specify ``RotationLambdaARN`` instead.
        :param rotate_immediately_on_update: Specifies whether to rotate the secret immediately or wait until the next scheduled rotation window. The rotation schedule is defined in ``RotationRules`` . If you don't immediately rotate the secret, Secrets Manager tests the rotation configuration by running the ```testSecret`` step <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ of the Lambda rotation function. The test creates an ``AWSPENDING`` version of the secret and then removes it. If you don't specify this value, then by default, Secrets Manager rotates the secret immediately. Rotation is an asynchronous process. For more information, see `How rotation works <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ .
        :param rotation_lambda_arn: The ARN of an existing Lambda rotation function. To specify a rotation function that is also defined in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function. To create a new rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ , specify ``HostedRotationLambda`` instead.
        :param rotation_rules: A structure that defines the rotation configuration for this secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            cfn_rotation_schedule_props = secretsmanager.CfnRotationScheduleProps(
                secret_id="secretId",
            
                # the properties below are optional
                hosted_rotation_lambda=secretsmanager.CfnRotationSchedule.HostedRotationLambdaProperty(
                    rotation_type="rotationType",
            
                    # the properties below are optional
                    exclude_characters="excludeCharacters",
                    kms_key_arn="kmsKeyArn",
                    master_secret_arn="masterSecretArn",
                    master_secret_kms_key_arn="masterSecretKmsKeyArn",
                    rotation_lambda_name="rotationLambdaName",
                    superuser_secret_arn="superuserSecretArn",
                    superuser_secret_kms_key_arn="superuserSecretKmsKeyArn",
                    vpc_security_group_ids="vpcSecurityGroupIds",
                    vpc_subnet_ids="vpcSubnetIds"
                ),
                rotate_immediately_on_update=False,
                rotation_lambda_arn="rotationLambdaArn",
                rotation_rules=secretsmanager.CfnRotationSchedule.RotationRulesProperty(
                    automatically_after_days=123,
                    duration="duration",
                    schedule_expression="scheduleExpression"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee97b74cc1d45e9e48f06df1f73390ea9a6584614534e1f4f3ea666f4830d69)
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument hosted_rotation_lambda", value=hosted_rotation_lambda, expected_type=type_hints["hosted_rotation_lambda"])
            check_type(argname="argument rotate_immediately_on_update", value=rotate_immediately_on_update, expected_type=type_hints["rotate_immediately_on_update"])
            check_type(argname="argument rotation_lambda_arn", value=rotation_lambda_arn, expected_type=type_hints["rotation_lambda_arn"])
            check_type(argname="argument rotation_rules", value=rotation_rules, expected_type=type_hints["rotation_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_id": secret_id,
        }
        if hosted_rotation_lambda is not None:
            self._values["hosted_rotation_lambda"] = hosted_rotation_lambda
        if rotate_immediately_on_update is not None:
            self._values["rotate_immediately_on_update"] = rotate_immediately_on_update
        if rotation_lambda_arn is not None:
            self._values["rotation_lambda_arn"] = rotation_lambda_arn
        if rotation_rules is not None:
            self._values["rotation_rules"] = rotation_rules

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''The ARN or name of the secret to rotate.

        To reference a secret also created in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hosted_rotation_lambda(
        self,
    ) -> typing.Optional[typing.Union[CfnRotationSchedule.HostedRotationLambdaProperty, _IResolvable_a771d0ef]]:
        '''Creates a new Lambda rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ . To use a rotation function that already exists, specify ``RotationLambdaARN`` instead.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda
        '''
        result = self._values.get("hosted_rotation_lambda")
        return typing.cast(typing.Optional[typing.Union[CfnRotationSchedule.HostedRotationLambdaProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def rotate_immediately_on_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to rotate the secret immediately or wait until the next scheduled rotation window.

        The rotation schedule is defined in ``RotationRules`` .

        If you don't immediately rotate the secret, Secrets Manager tests the rotation configuration by running the ```testSecret`` step <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ of the Lambda rotation function. The test creates an ``AWSPENDING`` version of the secret and then removes it.

        If you don't specify this value, then by default, Secrets Manager rotates the secret immediately.

        Rotation is an asynchronous process. For more information, see `How rotation works <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotateimmediatelyonupdate
        '''
        result = self._values.get("rotate_immediately_on_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def rotation_lambda_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an existing Lambda rotation function.

        To specify a rotation function that is also defined in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function.

        To create a new rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ , specify ``HostedRotationLambda`` instead.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        '''
        result = self._values.get("rotation_lambda_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_rules(
        self,
    ) -> typing.Optional[typing.Union[CfnRotationSchedule.RotationRulesProperty, _IResolvable_a771d0ef]]:
        '''A structure that defines the rotation configuration for this secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        '''
        result = self._values.get("rotation_rules")
        return typing.cast(typing.Optional[typing.Union[CfnRotationSchedule.RotationRulesProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRotationScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSecret(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.CfnSecret",
):
    '''A CloudFormation ``AWS::SecretsManager::Secret``.

    Creates a new secret. A *secret* can be a password, a set of credentials such as a user name and password, an OAuth token, or other secret information that you store in an encrypted form in Secrets Manager.

    To retrieve a secret in a CloudFormation template, use a *dynamic reference* . For more information, see `Retrieve a secret in an AWS CloudFormation resource <https://docs.aws.amazon.com/secretsmanager/latest/userguide/cfn-example_reference-secret.html>`_ .

    A common scenario is to first create a secret with ``GenerateSecretString`` , which generates a password, and then use a dynamic reference to retrieve the username and password from the secret to use as credentials for a new database. Follow these steps, as shown in the examples below:

    - Define the secret without referencing the service or database. You can't reference the service or database because it doesn't exist yet. The secret must contain a username and password.
    - Next, define the service or database. Include the reference to the secret to use stored credentials to define the database admin user and password.
    - Finally, define a ``SecretTargetAttachment`` resource type to finish configuring the secret with the required database engine type and the connection details of the service or database. The rotation function requires the details, if you attach one later by defining a `AWS::SecretsManager::RotationSchedule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html>`_ resource type.

    For information about creating a secret in the console, see `Create a secret <https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_create-basic-secret.html>`_ . For information about creating a secret using the CLI or SDK, see `CreateSecret <https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_CreateSecret.html>`_ .

    For information about retrieving a secret in code, see `Retrieve secrets from Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets.html>`_ .
    .. epigraph::

       Do not create a dynamic reference using a backslash ``(\\)`` as the final value. AWS CloudFormation cannot resolve those references, which causes a resource failure.

    :cloudformationResource: AWS::SecretsManager::Secret
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_secretsmanager as secretsmanager
        
        cfn_secret = secretsmanager.CfnSecret(self, "MyCfnSecret",
            description="description",
            generate_secret_string=secretsmanager.CfnSecret.GenerateSecretStringProperty(
                exclude_characters="excludeCharacters",
                exclude_lowercase=False,
                exclude_numbers=False,
                exclude_punctuation=False,
                exclude_uppercase=False,
                generate_string_key="generateStringKey",
                include_space=False,
                password_length=123,
                require_each_included_type=False,
                secret_string_template="secretStringTemplate"
            ),
            kms_key_id="kmsKeyId",
            name="name",
            replica_regions=[secretsmanager.CfnSecret.ReplicaRegionProperty(
                region="region",
        
                # the properties below are optional
                kms_key_id="kmsKeyId"
            )],
            secret_string="secretString",
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
        description: typing.Optional[builtins.str] = None,
        generate_secret_string: typing.Optional[typing.Union[typing.Union["CfnSecret.GenerateSecretStringProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        replica_regions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSecret.ReplicaRegionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        secret_string: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SecretsManager::Secret``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: The description of the secret.
        :param generate_secret_string: A structure that specifies how to generate a password to encrypt and store in the secret. To include a specific string in the secret, use ``SecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret. We recommend that you specify the maximum length and include every character type that the system you are generating a password for can support.
        :param kms_key_id: The ARN, key ID, or alias of the AWS KMS key that Secrets Manager uses to encrypt the secret value in the secret. An alias is always prefixed by ``alias/`` , for example ``alias/aws/secretsmanager`` . For more information, see `About aliases <https://docs.aws.amazon.com/kms/latest/developerguide/alias-about.html>`_ . To use a AWS KMS key in a different account, use the key ARN or the alias ARN. If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If that key doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value. If the secret is in a different AWS account from the credentials calling the API, then you can't use ``aws/secretsmanager`` to encrypt the secret, and you must create and use a customer managed AWS KMS key.
        :param name: The name of the new secret. The secret name can contain ASCII letters, numbers, and the following characters: /_+=.@- Do not end your secret name with a hyphen followed by six characters. If you do so, you risk confusion and unexpected results when searching for a secret by partial ARN. Secrets Manager automatically adds a hyphen and six random characters after the secret name at the end of the ARN.
        :param replica_regions: A custom type that specifies a ``Region`` and the ``KmsKeyId`` for a replica secret.
        :param secret_string: The text to encrypt and store in the secret. We recommend you use a JSON structure of key/value pairs for your secret value. To generate a random password, use ``GenerateSecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret.
        :param tags: A list of tags to attach to the secret. Each tag is a key and value pair of strings in a JSON text string, for example: ``[{"Key":"CostCenter","Value":"12345"},{"Key":"environment","Value":"production"}]`` Secrets Manager tag key names are case sensitive. A tag with the key "ABC" is a different tag from one with key "abc". If you check tags in permissions policies as part of your security strategy, then adding or removing a tag can change permissions. If the completion of this operation would result in you losing your permissions for this secret, then Secrets Manager blocks the operation and returns an ``Access Denied`` error. For more information, see `Control access to secrets using tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#tag-secrets-abac>`_ and `Limit access to identities with tags that match secrets' tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#auth-and-access_tags2>`_ . For information about how to format a JSON parameter for the various command line tool environments, see `Using JSON for Parameters <https://docs.aws.amazon.com/cli/latest/userguide/cli-using-param.html#cli-using-param-json>`_ . If your command-line tool or SDK requires quotation marks around the parameter, you should use single quotes to avoid confusion with the double quotes required in the JSON text. The following restrictions apply to tags: - Maximum number of tags per secret: 50 - Maximum key length: 127 Unicode characters in UTF-8 - Maximum value length: 255 Unicode characters in UTF-8 - Tag keys and values are case sensitive. - Do not use the ``aws:`` prefix in your tag names or values because AWS reserves it for AWS use. You can't edit or delete tag names or values with this prefix. Tags with this prefix do not count against your tags per secret limit. - If you use your tagging schema across multiple services and resources, other services might have restrictions on allowed characters. Generally allowed characters: letters, spaces, and numbers representable in UTF-8, plus the following special characters: + - = . _ : / @.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e1150daf1664acc1182e989d5df4fba0ab6e0a84f83086637b4df790b74f93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecretProps(
            description=description,
            generate_secret_string=generate_secret_string,
            kms_key_id=kms_key_id,
            name=name,
            replica_regions=replica_regions,
            secret_string=secret_string,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d2977b221cc0094de62190cd9c7776223cacd8c1451efc2a80958047fe8446)
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
            type_hints = typing.get_type_hints(_typecheckingstub__590f95da6aefde77dee3040ecaf45cbac54a2d8267737cefcbf6e0f8540acdaa)
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
        '''A list of tags to attach to the secret.

        Each tag is a key and value pair of strings in a JSON text string, for example:

        ``[{"Key":"CostCenter","Value":"12345"},{"Key":"environment","Value":"production"}]``

        Secrets Manager tag key names are case sensitive. A tag with the key "ABC" is a different tag from one with key "abc".

        If you check tags in permissions policies as part of your security strategy, then adding or removing a tag can change permissions. If the completion of this operation would result in you losing your permissions for this secret, then Secrets Manager blocks the operation and returns an ``Access Denied`` error. For more information, see `Control access to secrets using tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#tag-secrets-abac>`_ and `Limit access to identities with tags that match secrets' tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#auth-and-access_tags2>`_ .

        For information about how to format a JSON parameter for the various command line tool environments, see `Using JSON for Parameters <https://docs.aws.amazon.com/cli/latest/userguide/cli-using-param.html#cli-using-param-json>`_ . If your command-line tool or SDK requires quotation marks around the parameter, you should use single quotes to avoid confusion with the double quotes required in the JSON text.

        The following restrictions apply to tags:

        - Maximum number of tags per secret: 50
        - Maximum key length: 127 Unicode characters in UTF-8
        - Maximum value length: 255 Unicode characters in UTF-8
        - Tag keys and values are case sensitive.
        - Do not use the ``aws:`` prefix in your tag names or values because AWS reserves it for AWS use. You can't edit or delete tag names or values with this prefix. Tags with this prefix do not count against your tags per secret limit.
        - If you use your tagging schema across multiple services and resources, other services might have restrictions on allowed characters. Generally allowed characters: letters, spaces, and numbers representable in UTF-8, plus the following special characters: + - = . _ : / @.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d250ba407e5e4bf985dc9770e5bcdc6fa1481feb04757fa42a924ee68d7bfb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="generateSecretString")
    def generate_secret_string(
        self,
    ) -> typing.Optional[typing.Union["CfnSecret.GenerateSecretStringProperty", _IResolvable_a771d0ef]]:
        '''A structure that specifies how to generate a password to encrypt and store in the secret.

        To include a specific string in the secret, use ``SecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret.

        We recommend that you specify the maximum length and include every character type that the system you are generating a password for can support.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSecret.GenerateSecretStringProperty", _IResolvable_a771d0ef]], jsii.get(self, "generateSecretString"))

    @generate_secret_string.setter
    def generate_secret_string(
        self,
        value: typing.Optional[typing.Union["CfnSecret.GenerateSecretStringProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6239caa307d8062a5c61bb36b6122bc7ed08512ca441a98da03b62e91fe74d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateSecretString", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ARN, key ID, or alias of the AWS KMS key that Secrets Manager uses to encrypt the secret value in the secret.

        An alias is always prefixed by ``alias/`` , for example ``alias/aws/secretsmanager`` . For more information, see `About aliases <https://docs.aws.amazon.com/kms/latest/developerguide/alias-about.html>`_ .

        To use a AWS KMS key in a different account, use the key ARN or the alias ARN.

        If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If that key doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.

        If the secret is in a different AWS account from the credentials calling the API, then you can't use ``aws/secretsmanager`` to encrypt the secret, and you must create and use a customer managed AWS KMS key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6dc1f75fc7fa7ce0c2d225bc315a54fd0bd9bd9ddea9c5fd9917f277abf0186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new secret.

        The secret name can contain ASCII letters, numbers, and the following characters: /_+=.@-

        Do not end your secret name with a hyphen followed by six characters. If you do so, you risk confusion and unexpected results when searching for a secret by partial ARN. Secrets Manager automatically adds a hyphen and six random characters after the secret name at the end of the ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b9fcbacdab823c3e3e122bc2d2c03afce669a172f5b6aad05023056a06550b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="replicaRegions")
    def replica_regions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSecret.ReplicaRegionProperty", _IResolvable_a771d0ef]]]]:
        '''A custom type that specifies a ``Region`` and the ``KmsKeyId`` for a replica secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-replicaregions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSecret.ReplicaRegionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "replicaRegions"))

    @replica_regions.setter
    def replica_regions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSecret.ReplicaRegionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2563a98b30aab3cde3787db85a2a8125a48e12191fb1d39b28837e171a1be364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaRegions", value)

    @builtins.property
    @jsii.member(jsii_name="secretString")
    def secret_string(self) -> typing.Optional[builtins.str]:
        '''The text to encrypt and store in the secret.

        We recommend you use a JSON structure of key/value pairs for your secret value. To generate a random password, use ``GenerateSecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretString"))

    @secret_string.setter
    def secret_string(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e219663b233e1359842bf37fde5846c36b5595df0b4e2fb6b5e11cef868797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretString", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_secretsmanager.CfnSecret.GenerateSecretStringProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_characters": "excludeCharacters",
            "exclude_lowercase": "excludeLowercase",
            "exclude_numbers": "excludeNumbers",
            "exclude_punctuation": "excludePunctuation",
            "exclude_uppercase": "excludeUppercase",
            "generate_string_key": "generateStringKey",
            "include_space": "includeSpace",
            "password_length": "passwordLength",
            "require_each_included_type": "requireEachIncludedType",
            "secret_string_template": "secretStringTemplate",
        },
    )
    class GenerateSecretStringProperty:
        def __init__(
            self,
            *,
            exclude_characters: typing.Optional[builtins.str] = None,
            exclude_lowercase: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            exclude_numbers: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            exclude_punctuation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            exclude_uppercase: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            generate_string_key: typing.Optional[builtins.str] = None,
            include_space: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            password_length: typing.Optional[jsii.Number] = None,
            require_each_included_type: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            secret_string_template: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Generates a random password.

            We recommend that you specify the maximum length and include every character type that the system you are generating a password for can support.

            *Required permissions:* ``secretsmanager:GetRandomPassword`` . For more information, see `IAM policy actions for Secrets Manager <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssecretsmanager.html#awssecretsmanager-actions-as-permissions>`_ and `Authentication and access control in Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html>`_ .

            :param exclude_characters: A string of the characters that you don't want in the password.
            :param exclude_lowercase: Specifies whether to exclude lowercase letters from the password. If you don't include this switch, the password can contain lowercase letters.
            :param exclude_numbers: Specifies whether to exclude numbers from the password. If you don't include this switch, the password can contain numbers.
            :param exclude_punctuation: Specifies whether to exclude the following punctuation characters from the password: `! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ `` { | } ~`` . If you don't include this switch, the password can contain punctuation.
            :param exclude_uppercase: Specifies whether to exclude uppercase letters from the password. If you don't include this switch, the password can contain uppercase letters.
            :param generate_string_key: The JSON key name for the key/value pair, where the value is the generated password. This pair is added to the JSON structure specified by the ``SecretStringTemplate`` parameter. If you specify this parameter, then you must also specify ``SecretStringTemplate`` .
            :param include_space: Specifies whether to include the space character. If you include this switch, the password can contain space characters.
            :param password_length: The length of the password. If you don't include this parameter, the default length is 32 characters.
            :param require_each_included_type: Specifies whether to include at least one upper and lowercase letter, one number, and one punctuation. If you don't include this switch, the password contains at least one of every character type.
            :param secret_string_template: A template that the generated string must match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_secretsmanager as secretsmanager
                
                generate_secret_string_property = secretsmanager.CfnSecret.GenerateSecretStringProperty(
                    exclude_characters="excludeCharacters",
                    exclude_lowercase=False,
                    exclude_numbers=False,
                    exclude_punctuation=False,
                    exclude_uppercase=False,
                    generate_string_key="generateStringKey",
                    include_space=False,
                    password_length=123,
                    require_each_included_type=False,
                    secret_string_template="secretStringTemplate"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4a6d449671a19ac5f72658c5f15bccdea8c610490498bf347b7c2ccd48da9b4)
                check_type(argname="argument exclude_characters", value=exclude_characters, expected_type=type_hints["exclude_characters"])
                check_type(argname="argument exclude_lowercase", value=exclude_lowercase, expected_type=type_hints["exclude_lowercase"])
                check_type(argname="argument exclude_numbers", value=exclude_numbers, expected_type=type_hints["exclude_numbers"])
                check_type(argname="argument exclude_punctuation", value=exclude_punctuation, expected_type=type_hints["exclude_punctuation"])
                check_type(argname="argument exclude_uppercase", value=exclude_uppercase, expected_type=type_hints["exclude_uppercase"])
                check_type(argname="argument generate_string_key", value=generate_string_key, expected_type=type_hints["generate_string_key"])
                check_type(argname="argument include_space", value=include_space, expected_type=type_hints["include_space"])
                check_type(argname="argument password_length", value=password_length, expected_type=type_hints["password_length"])
                check_type(argname="argument require_each_included_type", value=require_each_included_type, expected_type=type_hints["require_each_included_type"])
                check_type(argname="argument secret_string_template", value=secret_string_template, expected_type=type_hints["secret_string_template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_characters is not None:
                self._values["exclude_characters"] = exclude_characters
            if exclude_lowercase is not None:
                self._values["exclude_lowercase"] = exclude_lowercase
            if exclude_numbers is not None:
                self._values["exclude_numbers"] = exclude_numbers
            if exclude_punctuation is not None:
                self._values["exclude_punctuation"] = exclude_punctuation
            if exclude_uppercase is not None:
                self._values["exclude_uppercase"] = exclude_uppercase
            if generate_string_key is not None:
                self._values["generate_string_key"] = generate_string_key
            if include_space is not None:
                self._values["include_space"] = include_space
            if password_length is not None:
                self._values["password_length"] = password_length
            if require_each_included_type is not None:
                self._values["require_each_included_type"] = require_each_included_type
            if secret_string_template is not None:
                self._values["secret_string_template"] = secret_string_template

        @builtins.property
        def exclude_characters(self) -> typing.Optional[builtins.str]:
            '''A string of the characters that you don't want in the password.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludecharacters
            '''
            result = self._values.get("exclude_characters")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_lowercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to exclude lowercase letters from the password.

            If you don't include this switch, the password can contain lowercase letters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludelowercase
            '''
            result = self._values.get("exclude_lowercase")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def exclude_numbers(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to exclude numbers from the password.

            If you don't include this switch, the password can contain numbers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludenumbers
            '''
            result = self._values.get("exclude_numbers")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def exclude_punctuation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to exclude the following punctuation characters from the password: `!

            " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ `` { | } ~`` . If you don't include this switch, the password can contain punctuation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludepunctuation
            '''
            result = self._values.get("exclude_punctuation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def exclude_uppercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to exclude uppercase letters from the password.

            If you don't include this switch, the password can contain uppercase letters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludeuppercase
            '''
            result = self._values.get("exclude_uppercase")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def generate_string_key(self) -> typing.Optional[builtins.str]:
            '''The JSON key name for the key/value pair, where the value is the generated password.

            This pair is added to the JSON structure specified by the ``SecretStringTemplate`` parameter. If you specify this parameter, then you must also specify ``SecretStringTemplate`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-generatestringkey
            '''
            result = self._values.get("generate_string_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_space(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to include the space character.

            If you include this switch, the password can contain space characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-includespace
            '''
            result = self._values.get("include_space")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def password_length(self) -> typing.Optional[jsii.Number]:
            '''The length of the password.

            If you don't include this parameter, the default length is 32 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-passwordlength
            '''
            result = self._values.get("password_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def require_each_included_type(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to include at least one upper and lowercase letter, one number, and one punctuation.

            If you don't include this switch, the password contains at least one of every character type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-requireeachincludedtype
            '''
            result = self._values.get("require_each_included_type")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def secret_string_template(self) -> typing.Optional[builtins.str]:
            '''A template that the generated string must match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-secretstringtemplate
            '''
            result = self._values.get("secret_string_template")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GenerateSecretStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_secretsmanager.CfnSecret.ReplicaRegionProperty",
        jsii_struct_bases=[],
        name_mapping={"region": "region", "kms_key_id": "kmsKeyId"},
    )
    class ReplicaRegionProperty:
        def __init__(
            self,
            *,
            region: builtins.str,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a ``Region`` and the ``KmsKeyId`` for a replica secret.

            :param region: (Optional) A string that represents a ``Region`` , for example "us-east-1".
            :param kms_key_id: The ARN, key ID, or alias of the KMS key to encrypt the secret. If you don't include this field, Secrets Manager uses ``aws/secretsmanager`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-replicaregion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_secretsmanager as secretsmanager
                
                replica_region_property = secretsmanager.CfnSecret.ReplicaRegionProperty(
                    region="region",
                
                    # the properties below are optional
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b63288429b6aeb267cec681ce097a093d94edc0799ccfa68a089c2e0be35d3b7)
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "region": region,
            }
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def region(self) -> builtins.str:
            '''(Optional) A string that represents a ``Region`` , for example "us-east-1".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-replicaregion.html#cfn-secretsmanager-secret-replicaregion-region
            '''
            result = self._values.get("region")
            assert result is not None, "Required property 'region' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ARN, key ID, or alias of the KMS key to encrypt the secret.

            If you don't include this field, Secrets Manager uses ``aws/secretsmanager`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-replicaregion.html#cfn-secretsmanager-secret-replicaregion-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaRegionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.CfnSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "generate_secret_string": "generateSecretString",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "replica_regions": "replicaRegions",
        "secret_string": "secretString",
        "tags": "tags",
    },
)
class CfnSecretProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        generate_secret_string: typing.Optional[typing.Union[typing.Union[CfnSecret.GenerateSecretStringProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        replica_regions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSecret.ReplicaRegionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        secret_string: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSecret``.

        :param description: The description of the secret.
        :param generate_secret_string: A structure that specifies how to generate a password to encrypt and store in the secret. To include a specific string in the secret, use ``SecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret. We recommend that you specify the maximum length and include every character type that the system you are generating a password for can support.
        :param kms_key_id: The ARN, key ID, or alias of the AWS KMS key that Secrets Manager uses to encrypt the secret value in the secret. An alias is always prefixed by ``alias/`` , for example ``alias/aws/secretsmanager`` . For more information, see `About aliases <https://docs.aws.amazon.com/kms/latest/developerguide/alias-about.html>`_ . To use a AWS KMS key in a different account, use the key ARN or the alias ARN. If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If that key doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value. If the secret is in a different AWS account from the credentials calling the API, then you can't use ``aws/secretsmanager`` to encrypt the secret, and you must create and use a customer managed AWS KMS key.
        :param name: The name of the new secret. The secret name can contain ASCII letters, numbers, and the following characters: /_+=.@- Do not end your secret name with a hyphen followed by six characters. If you do so, you risk confusion and unexpected results when searching for a secret by partial ARN. Secrets Manager automatically adds a hyphen and six random characters after the secret name at the end of the ARN.
        :param replica_regions: A custom type that specifies a ``Region`` and the ``KmsKeyId`` for a replica secret.
        :param secret_string: The text to encrypt and store in the secret. We recommend you use a JSON structure of key/value pairs for your secret value. To generate a random password, use ``GenerateSecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret.
        :param tags: A list of tags to attach to the secret. Each tag is a key and value pair of strings in a JSON text string, for example: ``[{"Key":"CostCenter","Value":"12345"},{"Key":"environment","Value":"production"}]`` Secrets Manager tag key names are case sensitive. A tag with the key "ABC" is a different tag from one with key "abc". If you check tags in permissions policies as part of your security strategy, then adding or removing a tag can change permissions. If the completion of this operation would result in you losing your permissions for this secret, then Secrets Manager blocks the operation and returns an ``Access Denied`` error. For more information, see `Control access to secrets using tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#tag-secrets-abac>`_ and `Limit access to identities with tags that match secrets' tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#auth-and-access_tags2>`_ . For information about how to format a JSON parameter for the various command line tool environments, see `Using JSON for Parameters <https://docs.aws.amazon.com/cli/latest/userguide/cli-using-param.html#cli-using-param-json>`_ . If your command-line tool or SDK requires quotation marks around the parameter, you should use single quotes to avoid confusion with the double quotes required in the JSON text. The following restrictions apply to tags: - Maximum number of tags per secret: 50 - Maximum key length: 127 Unicode characters in UTF-8 - Maximum value length: 255 Unicode characters in UTF-8 - Tag keys and values are case sensitive. - Do not use the ``aws:`` prefix in your tag names or values because AWS reserves it for AWS use. You can't edit or delete tag names or values with this prefix. Tags with this prefix do not count against your tags per secret limit. - If you use your tagging schema across multiple services and resources, other services might have restrictions on allowed characters. Generally allowed characters: letters, spaces, and numbers representable in UTF-8, plus the following special characters: + - = . _ : / @.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            cfn_secret_props = secretsmanager.CfnSecretProps(
                description="description",
                generate_secret_string=secretsmanager.CfnSecret.GenerateSecretStringProperty(
                    exclude_characters="excludeCharacters",
                    exclude_lowercase=False,
                    exclude_numbers=False,
                    exclude_punctuation=False,
                    exclude_uppercase=False,
                    generate_string_key="generateStringKey",
                    include_space=False,
                    password_length=123,
                    require_each_included_type=False,
                    secret_string_template="secretStringTemplate"
                ),
                kms_key_id="kmsKeyId",
                name="name",
                replica_regions=[secretsmanager.CfnSecret.ReplicaRegionProperty(
                    region="region",
            
                    # the properties below are optional
                    kms_key_id="kmsKeyId"
                )],
                secret_string="secretString",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6800cd79b70824bb85a0a168d974da6297709622676ea47f0d6f6ef74ce1f99)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument generate_secret_string", value=generate_secret_string, expected_type=type_hints["generate_secret_string"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replica_regions", value=replica_regions, expected_type=type_hints["replica_regions"])
            check_type(argname="argument secret_string", value=secret_string, expected_type=type_hints["secret_string"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if generate_secret_string is not None:
            self._values["generate_secret_string"] = generate_secret_string
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if replica_regions is not None:
            self._values["replica_regions"] = replica_regions
        if secret_string is not None:
            self._values["secret_string"] = secret_string
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generate_secret_string(
        self,
    ) -> typing.Optional[typing.Union[CfnSecret.GenerateSecretStringProperty, _IResolvable_a771d0ef]]:
        '''A structure that specifies how to generate a password to encrypt and store in the secret.

        To include a specific string in the secret, use ``SecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret.

        We recommend that you specify the maximum length and include every character type that the system you are generating a password for can support.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        '''
        result = self._values.get("generate_secret_string")
        return typing.cast(typing.Optional[typing.Union[CfnSecret.GenerateSecretStringProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ARN, key ID, or alias of the AWS KMS key that Secrets Manager uses to encrypt the secret value in the secret.

        An alias is always prefixed by ``alias/`` , for example ``alias/aws/secretsmanager`` . For more information, see `About aliases <https://docs.aws.amazon.com/kms/latest/developerguide/alias-about.html>`_ .

        To use a AWS KMS key in a different account, use the key ARN or the alias ARN.

        If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If that key doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.

        If the secret is in a different AWS account from the credentials calling the API, then you can't use ``aws/secretsmanager`` to encrypt the secret, and you must create and use a customer managed AWS KMS key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new secret.

        The secret name can contain ASCII letters, numbers, and the following characters: /_+=.@-

        Do not end your secret name with a hyphen followed by six characters. If you do so, you risk confusion and unexpected results when searching for a secret by partial ARN. Secrets Manager automatically adds a hyphen and six random characters after the secret name at the end of the ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_regions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSecret.ReplicaRegionProperty, _IResolvable_a771d0ef]]]]:
        '''A custom type that specifies a ``Region`` and the ``KmsKeyId`` for a replica secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-replicaregions
        '''
        result = self._values.get("replica_regions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSecret.ReplicaRegionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def secret_string(self) -> typing.Optional[builtins.str]:
        '''The text to encrypt and store in the secret.

        We recommend you use a JSON structure of key/value pairs for your secret value. To generate a random password, use ``GenerateSecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        '''
        result = self._values.get("secret_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags to attach to the secret.

        Each tag is a key and value pair of strings in a JSON text string, for example:

        ``[{"Key":"CostCenter","Value":"12345"},{"Key":"environment","Value":"production"}]``

        Secrets Manager tag key names are case sensitive. A tag with the key "ABC" is a different tag from one with key "abc".

        If you check tags in permissions policies as part of your security strategy, then adding or removing a tag can change permissions. If the completion of this operation would result in you losing your permissions for this secret, then Secrets Manager blocks the operation and returns an ``Access Denied`` error. For more information, see `Control access to secrets using tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#tag-secrets-abac>`_ and `Limit access to identities with tags that match secrets' tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#auth-and-access_tags2>`_ .

        For information about how to format a JSON parameter for the various command line tool environments, see `Using JSON for Parameters <https://docs.aws.amazon.com/cli/latest/userguide/cli-using-param.html#cli-using-param-json>`_ . If your command-line tool or SDK requires quotation marks around the parameter, you should use single quotes to avoid confusion with the double quotes required in the JSON text.

        The following restrictions apply to tags:

        - Maximum number of tags per secret: 50
        - Maximum key length: 127 Unicode characters in UTF-8
        - Maximum value length: 255 Unicode characters in UTF-8
        - Tag keys and values are case sensitive.
        - Do not use the ``aws:`` prefix in your tag names or values because AWS reserves it for AWS use. You can't edit or delete tag names or values with this prefix. Tags with this prefix do not count against your tags per secret limit.
        - If you use your tagging schema across multiple services and resources, other services might have restrictions on allowed characters. Generally allowed characters: letters, spaces, and numbers representable in UTF-8, plus the following special characters: + - = . _ : / @.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSecretTargetAttachment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.CfnSecretTargetAttachment",
):
    '''A CloudFormation ``AWS::SecretsManager::SecretTargetAttachment``.

    The ``AWS::SecretsManager::SecretTargetAttachment`` resource completes the final link between a Secrets Manager secret and the associated database by adding the database connection information to the secret JSON. If you want to turn on automatic rotation for a database credential secret, the secret must contain the database connection information. For more information, see `JSON structure of Secrets Manager database credential secrets <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_secret_json_structure.html>`_ .

    :cloudformationResource: AWS::SecretsManager::SecretTargetAttachment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_secretsmanager as secretsmanager
        
        cfn_secret_target_attachment = secretsmanager.CfnSecretTargetAttachment(self, "MyCfnSecretTargetAttachment",
            secret_id="secretId",
            target_id="targetId",
            target_type="targetType"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        secret_id: builtins.str,
        target_id: builtins.str,
        target_type: builtins.str,
    ) -> None:
        '''Create a new ``AWS::SecretsManager::SecretTargetAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param secret_id: The ARN or name of the secret. To reference a secret also created in this template, use the see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.
        :param target_id: The ID of the database or cluster.
        :param target_type: A string that defines the type of service or database associated with the secret. This value instructs Secrets Manager how to update the secret with the details of the service or database. This value must be one of the following: - AWS::RDS::DBInstance - AWS::RDS::DBCluster - AWS::Redshift::Cluster - AWS::DocDB::DBInstance - AWS::DocDB::DBCluster
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227308d12a64af3b37b061d81d303772e178f78cfedb822e6311a75e3cf90677)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecretTargetAttachmentProps(
            secret_id=secret_id, target_id=target_id, target_type=target_type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f061fb1a3be887a3976c628757eafb259a6880e85c5f4a72b7dfdaaa275f9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0feae507db7721704a3c909aac4856c7c29d0680abb1f0d824a9f86f61e12241)
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
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        '''The ARN or name of the secret.

        To reference a secret also created in this template, use the see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d13b1cc0b7649bcd4b5031cf2fda6fa94302d0c79d17e324394439aac19ec54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value)

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        '''The ID of the database or cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetId"))

    @target_id.setter
    def target_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a163dcb6948283ee242a198eeb575a4dacc984e12d022c47790ef0a29edc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetId", value)

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> builtins.str:
        '''A string that defines the type of service or database associated with the secret.

        This value instructs Secrets Manager how to update the secret with the details of the service or database. This value must be one of the following:

        - AWS::RDS::DBInstance
        - AWS::RDS::DBCluster
        - AWS::Redshift::Cluster
        - AWS::DocDB::DBInstance
        - AWS::DocDB::DBCluster

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetType"))

    @target_type.setter
    def target_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc25b3a55c83c5ba0eb20565f36a37aaa66012b0b80fa8ad1541c695cab40512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetType", value)


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.CfnSecretTargetAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "target_id": "targetId",
        "target_type": "targetType",
    },
)
class CfnSecretTargetAttachmentProps:
    def __init__(
        self,
        *,
        secret_id: builtins.str,
        target_id: builtins.str,
        target_type: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnSecretTargetAttachment``.

        :param secret_id: The ARN or name of the secret. To reference a secret also created in this template, use the see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.
        :param target_id: The ID of the database or cluster.
        :param target_type: A string that defines the type of service or database associated with the secret. This value instructs Secrets Manager how to update the secret with the details of the service or database. This value must be one of the following: - AWS::RDS::DBInstance - AWS::RDS::DBCluster - AWS::Redshift::Cluster - AWS::DocDB::DBInstance - AWS::DocDB::DBCluster

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            cfn_secret_target_attachment_props = secretsmanager.CfnSecretTargetAttachmentProps(
                secret_id="secretId",
                target_id="targetId",
                target_type="targetType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c88e52141ebf2a6f7f26db037bf2076dd15a802934aa41047355654578d339)
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_id": secret_id,
            "target_id": target_id,
            "target_type": target_type,
        }

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''The ARN or name of the secret.

        To reference a secret also created in this template, use the see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_id(self) -> builtins.str:
        '''The ID of the database or cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        '''
        result = self._values.get("target_id")
        assert result is not None, "Required property 'target_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_type(self) -> builtins.str:
        '''A string that defines the type of service or database associated with the secret.

        This value instructs Secrets Manager how to update the secret with the details of the service or database. This value must be one of the following:

        - AWS::RDS::DBInstance
        - AWS::RDS::DBCluster
        - AWS::Redshift::Cluster
        - AWS::DocDB::DBInstance
        - AWS::DocDB::DBCluster

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        '''
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretTargetAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IConnectable_c1c0e72c)
class HostedRotation(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.HostedRotation",
):
    '''(experimental) A hosted rotation.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        secret = secretsmanager.Secret(self, "Secret")
        
        secret.add_rotation_schedule("RotationSchedule",
            hosted_rotation=secretsmanager.HostedRotation.mysql_single_user()
        )
    '''

    @jsii.member(jsii_name="mariaDbMultiUser")
    @builtins.classmethod
    def maria_db_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) MariaDB Multi User.

        :param master_secret: (experimental) The master secret for a multi user rotation scheme.
        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "mariaDbMultiUser", [options]))

    @jsii.member(jsii_name="mariaDbSingleUser")
    @builtins.classmethod
    def maria_db_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) MariaDB Single User.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "mariaDbSingleUser", [options]))

    @jsii.member(jsii_name="mongoDbMultiUser")
    @builtins.classmethod
    def mongo_db_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) MongoDB Multi User.

        :param master_secret: (experimental) The master secret for a multi user rotation scheme.
        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "mongoDbMultiUser", [options]))

    @jsii.member(jsii_name="mongoDbSingleUser")
    @builtins.classmethod
    def mongo_db_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) MongoDB Single User.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "mongoDbSingleUser", [options]))

    @jsii.member(jsii_name="mysqlMultiUser")
    @builtins.classmethod
    def mysql_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) MySQL Multi User.

        :param master_secret: (experimental) The master secret for a multi user rotation scheme.
        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "mysqlMultiUser", [options]))

    @jsii.member(jsii_name="mysqlSingleUser")
    @builtins.classmethod
    def mysql_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) MySQL Single User.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "mysqlSingleUser", [options]))

    @jsii.member(jsii_name="oracleMultiUser")
    @builtins.classmethod
    def oracle_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) Oracle Multi User.

        :param master_secret: (experimental) The master secret for a multi user rotation scheme.
        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "oracleMultiUser", [options]))

    @jsii.member(jsii_name="oracleSingleUser")
    @builtins.classmethod
    def oracle_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) Oracle Single User.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "oracleSingleUser", [options]))

    @jsii.member(jsii_name="postgreSqlMultiUser")
    @builtins.classmethod
    def postgre_sql_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) PostgreSQL Multi User.

        :param master_secret: (experimental) The master secret for a multi user rotation scheme.
        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "postgreSqlMultiUser", [options]))

    @jsii.member(jsii_name="postgreSqlSingleUser")
    @builtins.classmethod
    def postgre_sql_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) PostgreSQL Single User.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "postgreSqlSingleUser", [options]))

    @jsii.member(jsii_name="redshiftMultiUser")
    @builtins.classmethod
    def redshift_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) Redshift Multi User.

        :param master_secret: (experimental) The master secret for a multi user rotation scheme.
        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "redshiftMultiUser", [options]))

    @jsii.member(jsii_name="redshiftSingleUser")
    @builtins.classmethod
    def redshift_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) Redshift Single User.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "redshiftSingleUser", [options]))

    @jsii.member(jsii_name="sqlServerMultiUser")
    @builtins.classmethod
    def sql_server_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) SQL Server Multi User.

        :param master_secret: (experimental) The master secret for a multi user rotation scheme.
        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "sqlServerMultiUser", [options]))

    @jsii.member(jsii_name="sqlServerSingleUser")
    @builtins.classmethod
    def sql_server_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "HostedRotation":
        '''(experimental) SQL Server Single User.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("HostedRotation", jsii.sinvoke(cls, "sqlServerSingleUser", [options]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        secret: "ISecret",
        scope: _constructs_77d1e7e8.Construct,
    ) -> CfnRotationSchedule.HostedRotationLambdaProperty:
        '''(experimental) Binds this hosted rotation to a secret.

        :param secret: -
        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332e05edcf7cc25bd609fd447457c936c1f719460c14bd94c95935fe997f43b3)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(CfnRotationSchedule.HostedRotationLambdaProperty, jsii.invoke(self, "bind", [secret, scope]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) Security group connections for this hosted rotation.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))


class HostedRotationType(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.HostedRotationType",
):
    '''(experimental) Hosted rotation type.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_secretsmanager as secretsmanager
        
        hosted_rotation_type = secretsmanager.HostedRotationType.MARIADB_MULTI_USER
    '''

    @jsii.python.classproperty
    @jsii.member(jsii_name="MARIADB_MULTI_USER")
    def MARIADB_MULTI_USER(cls) -> "HostedRotationType":
        '''(experimental) MariaDB Multi User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "MARIADB_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MARIADB_SINGLE_USER")
    def MARIADB_SINGLE_USER(cls) -> "HostedRotationType":
        '''(experimental) MariaDB Single User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "MARIADB_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONGODB_MULTI_USER")
    def MONGODB_MULTI_USER(cls) -> "HostedRotationType":
        '''(experimental) MongoDB Multi User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "MONGODB_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONGODB_SINGLE_USER")
    def MONGODB_SINGLE_USER(cls) -> "HostedRotationType":
        '''(experimental) MongoDB Single User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "MONGODB_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MYSQL_MULTI_USER")
    def MYSQL_MULTI_USER(cls) -> "HostedRotationType":
        '''(experimental) MySQL Multi User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "MYSQL_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MYSQL_SINGLE_USER")
    def MYSQL_SINGLE_USER(cls) -> "HostedRotationType":
        '''(experimental) MySQL Single User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "MYSQL_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_MULTI_USER")
    def ORACLE_MULTI_USER(cls) -> "HostedRotationType":
        '''(experimental) Oracle Multi User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "ORACLE_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_SINGLE_USER")
    def ORACLE_SINGLE_USER(cls) -> "HostedRotationType":
        '''(experimental) Oracle Single User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "ORACLE_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="POSTGRESQL_MULTI_USER")
    def POSTGRESQL_MULTI_USER(cls) -> "HostedRotationType":
        '''(experimental) PostgreSQL Multi User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "POSTGRESQL_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="POSTGRESQL_SINGLE_USER")
    def POSTGRESQL_SINGLE_USER(cls) -> "HostedRotationType":
        '''(experimental) PostgreSQL Single User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "POSTGRESQL_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDSHIFT_MULTI_USER")
    def REDSHIFT_MULTI_USER(cls) -> "HostedRotationType":
        '''(experimental) Redshift Multi User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "REDSHIFT_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDSHIFT_SINGLE_USER")
    def REDSHIFT_SINGLE_USER(cls) -> "HostedRotationType":
        '''(experimental) Redshift Single User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "REDSHIFT_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQLSERVER_MULTI_USER")
    def SQLSERVER_MULTI_USER(cls) -> "HostedRotationType":
        '''(experimental) SQL Server Multi User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "SQLSERVER_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQLSERVER_SINGLE_USER")
    def SQLSERVER_SINGLE_USER(cls) -> "HostedRotationType":
        '''(experimental) SQL Server Single User.

        :stability: experimental
        '''
        return typing.cast("HostedRotationType", jsii.sget(cls, "SQLSERVER_SINGLE_USER"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The type of rotation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="isMultiUser")
    def is_multi_user(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the rotation uses the mutli user scheme.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "isMultiUser"))


@jsii.interface(jsii_type="monocdk.aws_secretsmanager.ISecret")
class ISecret(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A secret in AWS Secrets Manager.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        '''(experimental) The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        '''(experimental) The name of the secret.

        For "owned" secrets, this will be the full resource name (secret name + suffix), unless the
        '@aws-cdk/aws-secretsmanager:parseOwnedSecretName' feature flag is set.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _SecretValue_c18506ef:
        '''(experimental) Retrieve the value of the stored secret as a ``SecretValue``.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
    ) -> "RotationSchedule":
        '''(experimental) Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. A value of zero will disable automatic rotation - ``Duration.days(0)``. Default: Duration.days(30)
        :param hosted_rotation: (experimental) Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: (experimental) A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="attach")
    def attach(self, target: "ISecretAttachmentTarget") -> "ISecret":
        '''(experimental) Attach a target to this secret.

        :param target: The target to attach.

        :return: An attached secret

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        '''(experimental) Denies the ``DeleteSecret`` action to all principals within the current account.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_4c5a91d1,
        version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants reading the secret value to some role.

        :param grantee: the principal being granted permission.
        :param version_stages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants writing and updating the secret value to some role.

        :param grantee: the principal being granted permission.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, key: builtins.str) -> _SecretValue_c18506ef:
        '''(experimental) Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param key: -

        :stability: experimental
        '''
        ...


class _ISecretProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A secret in AWS Secrets Manager.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_secretsmanager.ISecret"

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        '''(experimental) The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        '''(experimental) The name of the secret.

        For "owned" secrets, this will be the full resource name (secret name + suffix), unless the
        '@aws-cdk/aws-secretsmanager:parseOwnedSecretName' feature flag is set.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _SecretValue_c18506ef:
        '''(experimental) Retrieve the value of the stored secret as a ``SecretValue``.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_SecretValue_c18506ef, jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretFullArn"))

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
    ) -> "RotationSchedule":
        '''(experimental) Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. A value of zero will disable automatic rotation - ``Duration.days(0)``. Default: Duration.days(30)
        :param hosted_rotation: (experimental) Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: (experimental) A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c584027a331b568c5553ab4136dc8cddb26dd42bf6e60c5d4607eaec8f7e29)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = RotationScheduleOptions(
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotation_lambda=rotation_lambda,
        )

        return typing.cast("RotationSchedule", jsii.invoke(self, "addRotationSchedule", [id, options]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e602c2044eca7da229fd242caf9dd48b37ab8a4498d2994b097db577791940)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="attach")
    def attach(self, target: "ISecretAttachmentTarget") -> ISecret:
        '''(experimental) Attach a target to this secret.

        :param target: The target to attach.

        :return: An attached secret

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8b8471522fdf309d1f5a6e4c15400bbf8fbdff2fe60649bdfca327a38b55e6)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(ISecret, jsii.invoke(self, "attach", [target]))

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        '''(experimental) Denies the ``DeleteSecret`` action to all principals within the current account.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "denyAccountRootDelete", []))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_4c5a91d1,
        version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants reading the secret value to some role.

        :param grantee: the principal being granted permission.
        :param version_stages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9341fe8876da08f94c51ab1668554157b497f515f319ef17cc48c47ec8aef15)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument version_stages", value=version_stages, expected_type=type_hints["version_stages"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee, version_stages]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants writing and updating the secret value to some role.

        :param grantee: the principal being granted permission.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e2ea86c5a628690e3f8078d34a08bf0735701c3b123ff5db4f59a89a5e2ce0)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, key: builtins.str) -> _SecretValue_c18506ef:
        '''(experimental) Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75485d103556923a9b50675ac451df40995da778166f60ccb4d53820c0bb11c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(_SecretValue_c18506ef, jsii.invoke(self, "secretValueFromJson", [key]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecret).__jsii_proxy_class__ = lambda : _ISecretProxy


@jsii.interface(jsii_type="monocdk.aws_secretsmanager.ISecretAttachmentTarget")
class ISecretAttachmentTarget(typing_extensions.Protocol):
    '''(experimental) A secret attachment target.

    :stability: experimental
    '''

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        '''(experimental) Renders the target specifications.

        :stability: experimental
        '''
        ...


class _ISecretAttachmentTargetProxy:
    '''(experimental) A secret attachment target.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_secretsmanager.ISecretAttachmentTarget"

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        '''(experimental) Renders the target specifications.

        :stability: experimental
        '''
        return typing.cast("SecretAttachmentTargetProps", jsii.invoke(self, "asSecretAttachmentTarget", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecretAttachmentTarget).__jsii_proxy_class__ = lambda : _ISecretAttachmentTargetProxy


@jsii.interface(jsii_type="monocdk.aws_secretsmanager.ISecretTargetAttachment")
class ISecretTargetAttachment(ISecret, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> builtins.str:
        '''(experimental) Same as ``secretArn``.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ISecretTargetAttachmentProxy(
    jsii.proxy_for(ISecret), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_secretsmanager.ISecretTargetAttachment"

    @builtins.property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> builtins.str:
        '''(experimental) Same as ``secretArn``.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretTargetAttachmentSecretArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecretTargetAttachment).__jsii_proxy_class__ = lambda : _ISecretTargetAttachmentProxy


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.ReplicaRegion",
    jsii_struct_bases=[],
    name_mapping={"region": "region", "encryption_key": "encryptionKey"},
)
class ReplicaRegion:
    def __init__(
        self,
        *,
        region: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
    ) -> None:
        '''(experimental) Secret replica region.

        :param region: (experimental) The name of the region.
        :param encryption_key: (experimental) The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_kms as kms
            from monocdk import aws_secretsmanager as secretsmanager
            
            # key: kms.Key
            
            replica_region = secretsmanager.ReplicaRegion(
                region="region",
            
                # the properties below are optional
                encryption_key=key
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e512691cba43679c69de55ff880e526f2584caf492dbd7a621846a83ecd5a1ce)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region": region,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) The name of the region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The customer-managed encryption key to use for encrypting the secret value.

        :default: - A default KMS key for the account and region is used.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReplicaRegion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourcePolicy(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.ResourcePolicy",
):
    '''(experimental) Resource Policy for SecretsManager Secrets.

    Policies define the operations that are allowed on this resource.

    You almost never need to define this construct directly.

    All AWS resources that support resource policies have a method called
    ``addToResourcePolicy()``, which will automatically create a new resource
    policy if one doesn't exist yet, otherwise it will add to the existing
    policy.

    Prefer to use ``addToResourcePolicy()`` instead.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_secretsmanager as secretsmanager
        
        # secret: secretsmanager.Secret
        
        resource_policy = secretsmanager.ResourcePolicy(self, "MyResourcePolicy",
            secret=secret
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        secret: ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param secret: (experimental) The secret to attach a resource-based permissions policy.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70938f171b6277261bcee1645321cafa60b767cf3fd1bda370a98172b7a21990)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ResourcePolicyProps(secret=secret)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> _PolicyDocument_b5de5177:
        '''(experimental) The IAM policy document for this policy.

        :stability: experimental
        '''
        return typing.cast(_PolicyDocument_b5de5177, jsii.get(self, "document"))


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.ResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret"},
)
class ResourcePolicyProps:
    def __init__(self, *, secret: ISecret) -> None:
        '''(experimental) Construction properties for a ResourcePolicy.

        :param secret: (experimental) The secret to attach a resource-based permissions policy.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            # secret: secretsmanager.Secret
            
            resource_policy_props = secretsmanager.ResourcePolicyProps(
                secret=secret
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393ff0d8d30f68e45e20ef7d14b5b51362f8777d9c921bc1ad3f079600eaba23)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }

    @builtins.property
    def secret(self) -> ISecret:
        '''(experimental) The secret to attach a resource-based permissions policy.

        :stability: experimental
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RotationSchedule(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.RotationSchedule",
):
    '''(experimental) A rotation schedule.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_lambda as lambda_
        from monocdk import aws_secretsmanager as secretsmanager
        
        # duration: monocdk.Duration
        # function_: lambda.Function
        # hosted_rotation: secretsmanager.HostedRotation
        # secret: secretsmanager.Secret
        
        rotation_schedule = secretsmanager.RotationSchedule(self, "MyRotationSchedule",
            secret=secret,
        
            # the properties below are optional
            automatically_after=duration,
            hosted_rotation=hosted_rotation,
            rotation_lambda=function_
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        secret: ISecret,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param secret: (experimental) The secret to rotate. If hosted rotation is used, this must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment`` or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. A value of zero will disable automatic rotation - ``Duration.days(0)``. Default: Duration.days(30)
        :param hosted_rotation: (experimental) Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: (experimental) A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01eef254b517f86b64586d47c9ddca0f881d46b9fbbeaee902e8f9773769c251)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RotationScheduleProps(
            secret=secret,
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotation_lambda=rotation_lambda,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.RotationScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "automatically_after": "automaticallyAfter",
        "hosted_rotation": "hostedRotation",
        "rotation_lambda": "rotationLambda",
    },
)
class RotationScheduleOptions:
    def __init__(
        self,
        *,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
    ) -> None:
        '''(experimental) Options to add a rotation schedule to a secret.

        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. A value of zero will disable automatic rotation - ``Duration.days(0)``. Default: Duration.days(30)
        :param hosted_rotation: (experimental) Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: (experimental) A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as lambda_
            
            # fn: lambda.Function
            
            secret = secretsmanager.Secret(self, "Secret")
            
            secret.add_rotation_schedule("RotationSchedule",
                rotation_lambda=fn,
                automatically_after=Duration.days(15)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6388f2e710db296a0664f7bf706e1434418e796cf2b17eb289ede17b724d8406)
            check_type(argname="argument automatically_after", value=automatically_after, expected_type=type_hints["automatically_after"])
            check_type(argname="argument hosted_rotation", value=hosted_rotation, expected_type=type_hints["hosted_rotation"])
            check_type(argname="argument rotation_lambda", value=rotation_lambda, expected_type=type_hints["rotation_lambda"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after
        if hosted_rotation is not None:
            self._values["hosted_rotation"] = hosted_rotation
        if rotation_lambda is not None:
            self._values["rotation_lambda"] = rotation_lambda

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        A value of zero will disable automatic rotation - ``Duration.days(0)``.

        :default: Duration.days(30)

        :stability: experimental
        '''
        result = self._values.get("automatically_after")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def hosted_rotation(self) -> typing.Optional[HostedRotation]:
        '''(experimental) Hosted rotation.

        :default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        result = self._values.get("hosted_rotation")
        return typing.cast(typing.Optional[HostedRotation], result)

    @builtins.property
    def rotation_lambda(self) -> typing.Optional[_IFunction_6e14f09e]:
        '''(experimental) A Lambda function that can rotate the secret.

        :default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        result = self._values.get("rotation_lambda")
        return typing.cast(typing.Optional[_IFunction_6e14f09e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.RotationScheduleProps",
    jsii_struct_bases=[RotationScheduleOptions],
    name_mapping={
        "automatically_after": "automaticallyAfter",
        "hosted_rotation": "hostedRotation",
        "rotation_lambda": "rotationLambda",
        "secret": "secret",
    },
)
class RotationScheduleProps(RotationScheduleOptions):
    def __init__(
        self,
        *,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
        secret: ISecret,
    ) -> None:
        '''(experimental) Construction properties for a RotationSchedule.

        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. A value of zero will disable automatic rotation - ``Duration.days(0)``. Default: Duration.days(30)
        :param hosted_rotation: (experimental) Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: (experimental) A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param secret: (experimental) The secret to rotate. If hosted rotation is used, this must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment`` or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_lambda as lambda_
            from monocdk import aws_secretsmanager as secretsmanager
            
            # duration: monocdk.Duration
            # function_: lambda.Function
            # hosted_rotation: secretsmanager.HostedRotation
            # secret: secretsmanager.Secret
            
            rotation_schedule_props = secretsmanager.RotationScheduleProps(
                secret=secret,
            
                # the properties below are optional
                automatically_after=duration,
                hosted_rotation=hosted_rotation,
                rotation_lambda=function_
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68355b16e6fca2935627847eb7b24318773346d156160bf5faa72c09ad87ab4)
            check_type(argname="argument automatically_after", value=automatically_after, expected_type=type_hints["automatically_after"])
            check_type(argname="argument hosted_rotation", value=hosted_rotation, expected_type=type_hints["hosted_rotation"])
            check_type(argname="argument rotation_lambda", value=rotation_lambda, expected_type=type_hints["rotation_lambda"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after
        if hosted_rotation is not None:
            self._values["hosted_rotation"] = hosted_rotation
        if rotation_lambda is not None:
            self._values["rotation_lambda"] = rotation_lambda

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        A value of zero will disable automatic rotation - ``Duration.days(0)``.

        :default: Duration.days(30)

        :stability: experimental
        '''
        result = self._values.get("automatically_after")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def hosted_rotation(self) -> typing.Optional[HostedRotation]:
        '''(experimental) Hosted rotation.

        :default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        result = self._values.get("hosted_rotation")
        return typing.cast(typing.Optional[HostedRotation], result)

    @builtins.property
    def rotation_lambda(self) -> typing.Optional[_IFunction_6e14f09e]:
        '''(experimental) A Lambda function that can rotate the secret.

        :default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        result = self._values.get("rotation_lambda")
        return typing.cast(typing.Optional[_IFunction_6e14f09e], result)

    @builtins.property
    def secret(self) -> ISecret:
        '''(experimental) The secret to rotate.

        If hosted rotation is used, this must be a JSON string with the following format::

           {
              "engine": <required: database engine>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port will be used>,
              "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords>
           }

        This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment``
        or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.

        :stability: experimental
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecret)
class Secret(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.Secret",
):
    '''(experimental) Creates a new secret in AWS SecretsManager.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Creates a new IAM user, access and secret keys, and stores the secret access key in a Secret.
        user = iam.User(self, "User")
        access_key = iam.AccessKey(self, "AccessKey", user=user)
        secret_value = secretsmanager.SecretStringValueBeta1.from_token(access_key.secret_access_key.to_string())
        secretsmanager.Secret(self, "Secret",
            secret_string_beta1=secret_value
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        generate_secret_string: typing.Optional[typing.Union["SecretStringGenerator", typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        replica_regions: typing.Optional[typing.Sequence[typing.Union[ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
        secret_name: typing.Optional[builtins.str] = None,
        secret_string_beta1: typing.Optional["SecretStringValueBeta1"] = None,
        secret_string_value: typing.Optional[_SecretValue_c18506ef] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: (experimental) An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: (experimental) The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: (experimental) Configuration for how to generate a secret value. Only one of ``secretString`` and ``generateSecretString`` can be provided. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param removal_policy: (experimental) Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param replica_regions: (experimental) A list of regions where to replicate this secret. Default: - Secret is not replicated
        :param secret_name: (experimental) A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        :param secret_string_beta1: (deprecated) Initial value for the secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret string -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies text data that you want to encrypt and store in this new version of the secret. May be a simple string value, or a string representation of a JSON structure. Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.
        :param secret_string_value: (experimental) Initial value for the secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret string -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies text data that you want to encrypt and store in this new version of the secret. May be a simple string value, or a string representation of a JSON structure. Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581e1f4f899e23c37781d58022f68e6e049ce0863aba6b4751cfa3a3c0e4e40e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecretProps(
            description=description,
            encryption_key=encryption_key,
            generate_secret_string=generate_secret_string,
            removal_policy=removal_policy,
            replica_regions=replica_regions,
            secret_name=secret_name,
            secret_string_beta1=secret_string_beta1,
            secret_string_value=secret_string_value,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretArn")
    @builtins.classmethod
    def from_secret_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        secret_arn: builtins.str,
    ) -> ISecret:
        '''
        :param scope: -
        :param id: -
        :param secret_arn: -

        :deprecated: use ``fromSecretCompleteArn`` or ``fromSecretPartialArn``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2550fba972082faed970e015a6121ae691fdd098fe490ab39845303c56a0a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
        return typing.cast(ISecret, jsii.sinvoke(cls, "fromSecretArn", [scope, id, secret_arn]))

    @jsii.member(jsii_name="fromSecretAttributes")
    @builtins.classmethod
    def from_secret_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        secret_arn: typing.Optional[builtins.str] = None,
        secret_complete_arn: typing.Optional[builtins.str] = None,
        secret_partial_arn: typing.Optional[builtins.str] = None,
    ) -> ISecret:
        '''(experimental) Import an existing secret into the Stack.

        :param scope: the scope of the import.
        :param id: the ID of the imported Secret in the construct tree.
        :param encryption_key: (experimental) The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.
        :param secret_arn: (deprecated) The ARN of the secret in SecretsManager. Cannot be used with ``secretCompleteArn`` or ``secretPartialArn``.
        :param secret_complete_arn: (experimental) The complete ARN of the secret in SecretsManager. This is the ARN including the Secrets Manager 6-character suffix. Cannot be used with ``secretArn`` or ``secretPartialArn``.
        :param secret_partial_arn: (experimental) The partial ARN of the secret in SecretsManager. This is the ARN without the Secrets Manager 6-character suffix. Cannot be used with ``secretArn`` or ``secretCompleteArn``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9238662dcf167408b8efa17536971f09089e40a5f3c0b2575446d908ff4b69e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = SecretAttributes(
            encryption_key=encryption_key,
            secret_arn=secret_arn,
            secret_complete_arn=secret_complete_arn,
            secret_partial_arn=secret_partial_arn,
        )

        return typing.cast(ISecret, jsii.sinvoke(cls, "fromSecretAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromSecretCompleteArn")
    @builtins.classmethod
    def from_secret_complete_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        secret_complete_arn: builtins.str,
    ) -> ISecret:
        '''(experimental) Imports a secret by complete ARN.

        The complete ARN is the ARN with the Secrets Manager-supplied suffix.

        :param scope: -
        :param id: -
        :param secret_complete_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9719bccc2c68509dd77d173bf0bf86686a759ce199549812aa59043b25a2d1f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret_complete_arn", value=secret_complete_arn, expected_type=type_hints["secret_complete_arn"])
        return typing.cast(ISecret, jsii.sinvoke(cls, "fromSecretCompleteArn", [scope, id, secret_complete_arn]))

    @jsii.member(jsii_name="fromSecretName")
    @builtins.classmethod
    def from_secret_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        secret_name: builtins.str,
    ) -> ISecret:
        '''(deprecated) Imports a secret by secret name;

        the ARN of the Secret will be set to the secret name.
        A secret with this name must exist in the same account & region.

        :param scope: -
        :param id: -
        :param secret_name: -

        :deprecated: use ``fromSecretNameV2``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e5304ba8babbcca0bcc0b1df44e50656db70a1c86599ed01b64b2098145dc2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        return typing.cast(ISecret, jsii.sinvoke(cls, "fromSecretName", [scope, id, secret_name]))

    @jsii.member(jsii_name="fromSecretNameV2")
    @builtins.classmethod
    def from_secret_name_v2(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        secret_name: builtins.str,
    ) -> ISecret:
        '''(experimental) Imports a secret by secret name.

        A secret with this name must exist in the same account & region.
        Replaces the deprecated ``fromSecretName``.

        :param scope: -
        :param id: -
        :param secret_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd50dc99b2558e5c0c9a49ab02673e024812a9ee6ed8ac718a3a079d9b6417d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        return typing.cast(ISecret, jsii.sinvoke(cls, "fromSecretNameV2", [scope, id, secret_name]))

    @jsii.member(jsii_name="fromSecretPartialArn")
    @builtins.classmethod
    def from_secret_partial_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        secret_partial_arn: builtins.str,
    ) -> ISecret:
        '''(experimental) Imports a secret by partial ARN.

        The partial ARN is the ARN without the Secrets Manager-supplied suffix.

        :param scope: -
        :param id: -
        :param secret_partial_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca3b70411703d8c5fad3c74972887cdebac0e93c03b74a686b4f9a68000b745)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret_partial_arn", value=secret_partial_arn, expected_type=type_hints["secret_partial_arn"])
        return typing.cast(ISecret, jsii.sinvoke(cls, "fromSecretPartialArn", [scope, id, secret_partial_arn]))

    @jsii.member(jsii_name="addReplicaRegion")
    def add_replica_region(
        self,
        region: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
    ) -> None:
        '''(experimental) Adds a replica region for the secret.

        :param region: The name of the region.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f6b493e93fa9ce7fc1db25841d8c46a5fb26eec8f7ffc750807845533581ec)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        return typing.cast(None, jsii.invoke(self, "addReplicaRegion", [region, encryption_key]))

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
    ) -> RotationSchedule:
        '''(experimental) Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. A value of zero will disable automatic rotation - ``Duration.days(0)``. Default: Duration.days(30)
        :param hosted_rotation: (experimental) Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: (experimental) A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19cfd234d06b6e4c6e6b2a2ed284fef12f295c0e1c711aed64479eb92552af1)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = RotationScheduleOptions(
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotation_lambda=rotation_lambda,
        )

        return typing.cast(RotationSchedule, jsii.invoke(self, "addRotationSchedule", [id, options]))

    @jsii.member(jsii_name="addTargetAttachment")
    def add_target_attachment(
        self,
        id: builtins.str,
        *,
        target: ISecretAttachmentTarget,
    ) -> "SecretTargetAttachment":
        '''(deprecated) Adds a target attachment to the secret.

        :param id: -
        :param target: (experimental) The target to attach the secret to.

        :return: an AttachedSecret

        :deprecated: use ``attach()`` instead

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646e258e3524cdd90fdc1671a07477000e88a22fdafe11030d03223ca3834e59)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = AttachedSecretOptions(target=target)

        return typing.cast("SecretTargetAttachment", jsii.invoke(self, "addTargetAttachment", [id, options]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce335e18cecee4638f0f5f0a2260935204f3789b37084350d900b10d12f991fd)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="attach")
    def attach(self, target: ISecretAttachmentTarget) -> ISecret:
        '''(experimental) Attach a target to this secret.

        :param target: The target to attach.

        :return: An attached secret

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4cbbb96001ec23848b7ebe26321b33cf6608bfad56b84148c8b2c5c7aa779c5)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(ISecret, jsii.invoke(self, "attach", [target]))

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        '''(experimental) Denies the ``DeleteSecret`` action to all principals within the current account.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "denyAccountRootDelete", []))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_4c5a91d1,
        version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813b2365bff6e358aed7f579fc6716e27eb4123fa6a5264642801eca2612359c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument version_stages", value=version_stages, expected_type=type_hints["version_stages"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee, version_stages]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants writing and updating the secret value to some role.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8e770fc6ea8f2de45ff4c2321dd87fcdc5d9c7a51a54a8ad64e44e2e1f93f6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, json_field: builtins.str) -> _SecretValue_c18506ef:
        '''(experimental) Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abdb9320e1abb09ce5768f350a5a17c831a1e3f45fe57f111999c9b8dc0f5859)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast(_SecretValue_c18506ef, jsii.invoke(self, "secretValueFromJson", [json_field]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="arnForPolicies")
    def _arn_for_policies(self) -> builtins.str:
        '''(experimental) Provides an identifier for this secret for use in IAM policies.

        If there is a full ARN, this is just the ARN;
        if we have a partial ARN -- due to either importing by secret name or partial ARN --
        then we need to add a suffix to capture the full ARN's format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arnForPolicies"))

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        '''(experimental) The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        '''(experimental) The name of the secret.

        For "owned" secrets, this will be the full resource name (secret name + suffix), unless the
        '@aws-cdk/aws-secretsmanager:parseOwnedSecretName' feature flag is set.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _SecretValue_c18506ef:
        '''(experimental) Retrieve the value of the stored secret as a ``SecretValue``.

        :stability: experimental
        '''
        return typing.cast(_SecretValue_c18506ef, jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretFullArn"))


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.SecretAttachmentTargetProps",
    jsii_struct_bases=[],
    name_mapping={"target_id": "targetId", "target_type": "targetType"},
)
class SecretAttachmentTargetProps:
    def __init__(
        self,
        *,
        target_id: builtins.str,
        target_type: AttachmentTargetType,
    ) -> None:
        '''(experimental) Attachment target specifications.

        :param target_id: (experimental) The id of the target to attach the secret to.
        :param target_type: (experimental) The type of the target to attach the secret to.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            secret_attachment_target_props = secretsmanager.SecretAttachmentTargetProps(
                target_id="targetId",
                target_type=secretsmanager.AttachmentTargetType.INSTANCE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618bb0d9f5849cf862d522a42acc9e20b275c65d9ec3a4dafef23dc7063ebec0)
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_id": target_id,
            "target_type": target_type,
        }

    @builtins.property
    def target_id(self) -> builtins.str:
        '''(experimental) The id of the target to attach the secret to.

        :stability: experimental
        '''
        result = self._values.get("target_id")
        assert result is not None, "Required property 'target_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_type(self) -> AttachmentTargetType:
        '''(experimental) The type of the target to attach the secret to.

        :stability: experimental
        '''
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return typing.cast(AttachmentTargetType, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretAttachmentTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.SecretAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_key": "encryptionKey",
        "secret_arn": "secretArn",
        "secret_complete_arn": "secretCompleteArn",
        "secret_partial_arn": "secretPartialArn",
    },
)
class SecretAttributes:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        secret_arn: typing.Optional[builtins.str] = None,
        secret_complete_arn: typing.Optional[builtins.str] = None,
        secret_partial_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attributes required to import an existing secret into the Stack.

        One ARN format (``secretArn``, ``secretCompleteArn``, ``secretPartialArn``) must be provided.

        :param encryption_key: (experimental) The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.
        :param secret_arn: (deprecated) The ARN of the secret in SecretsManager. Cannot be used with ``secretCompleteArn`` or ``secretPartialArn``.
        :param secret_complete_arn: (experimental) The complete ARN of the secret in SecretsManager. This is the ARN including the Secrets Manager 6-character suffix. Cannot be used with ``secretArn`` or ``secretPartialArn``.
        :param secret_partial_arn: (experimental) The partial ARN of the secret in SecretsManager. This is the ARN without the Secrets Manager 6-character suffix. Cannot be used with ``secretArn`` or ``secretCompleteArn``.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # encryption_key: kms.Key
            
            secret = secretsmanager.Secret.from_secret_attributes(self, "ImportedSecret",
                secret_arn="arn:aws:secretsmanager:<region>:<account-id-number>:secret:<secret-name>-<random-6-characters>",
                # If the secret is encrypted using a KMS-hosted CMK, either import or reference that key:
                encryption_key=encryption_key
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53c49bf7aa4c42fdf90269a1cc9647f7af714a54e8403135eb306c42f5aa8bc)
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument secret_complete_arn", value=secret_complete_arn, expected_type=type_hints["secret_complete_arn"])
            check_type(argname="argument secret_partial_arn", value=secret_partial_arn, expected_type=type_hints["secret_partial_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if secret_arn is not None:
            self._values["secret_arn"] = secret_arn
        if secret_complete_arn is not None:
            self._values["secret_complete_arn"] = secret_complete_arn
        if secret_partial_arn is not None:
            self._values["secret_partial_arn"] = secret_partial_arn

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def secret_arn(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The ARN of the secret in SecretsManager.

        Cannot be used with ``secretCompleteArn`` or ``secretPartialArn``.

        :deprecated: use ``secretCompleteArn`` or ``secretPartialArn`` instead.

        :stability: deprecated
        '''
        result = self._values.get("secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_complete_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The complete ARN of the secret in SecretsManager.

        This is the ARN including the Secrets Manager 6-character suffix.
        Cannot be used with ``secretArn`` or ``secretPartialArn``.

        :stability: experimental
        '''
        result = self._values.get("secret_complete_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_partial_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The partial ARN of the secret in SecretsManager.

        This is the ARN without the Secrets Manager 6-character suffix.
        Cannot be used with ``secretArn`` or ``secretCompleteArn``.

        :stability: experimental
        '''
        result = self._values.get("secret_partial_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.SecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "encryption_key": "encryptionKey",
        "generate_secret_string": "generateSecretString",
        "removal_policy": "removalPolicy",
        "replica_regions": "replicaRegions",
        "secret_name": "secretName",
        "secret_string_beta1": "secretStringBeta1",
        "secret_string_value": "secretStringValue",
    },
)
class SecretProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        generate_secret_string: typing.Optional[typing.Union["SecretStringGenerator", typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        replica_regions: typing.Optional[typing.Sequence[typing.Union[ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
        secret_name: typing.Optional[builtins.str] = None,
        secret_string_beta1: typing.Optional["SecretStringValueBeta1"] = None,
        secret_string_value: typing.Optional[_SecretValue_c18506ef] = None,
    ) -> None:
        '''(experimental) The properties required to create a new secret in AWS Secrets Manager.

        :param description: (experimental) An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: (experimental) The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: (experimental) Configuration for how to generate a secret value. Only one of ``secretString`` and ``generateSecretString`` can be provided. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param removal_policy: (experimental) Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param replica_regions: (experimental) A list of regions where to replicate this secret. Default: - Secret is not replicated
        :param secret_name: (experimental) A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        :param secret_string_beta1: (deprecated) Initial value for the secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret string -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies text data that you want to encrypt and store in this new version of the secret. May be a simple string value, or a string representation of a JSON structure. Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.
        :param secret_string_value: (experimental) Initial value for the secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret string -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies text data that you want to encrypt and store in this new version of the secret. May be a simple string value, or a string representation of a JSON structure. Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Creates a new IAM user, access and secret keys, and stores the secret access key in a Secret.
            user = iam.User(self, "User")
            access_key = iam.AccessKey(self, "AccessKey", user=user)
            secret_value = secretsmanager.SecretStringValueBeta1.from_token(access_key.secret_access_key.to_string())
            secretsmanager.Secret(self, "Secret",
                secret_string_beta1=secret_value
            )
        '''
        if isinstance(generate_secret_string, dict):
            generate_secret_string = SecretStringGenerator(**generate_secret_string)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24014daa44bb1f4d8d1a045f2864ba227b710f57fda38b3fe3494207dcd3f1ed)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument generate_secret_string", value=generate_secret_string, expected_type=type_hints["generate_secret_string"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument replica_regions", value=replica_regions, expected_type=type_hints["replica_regions"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument secret_string_beta1", value=secret_string_beta1, expected_type=type_hints["secret_string_beta1"])
            check_type(argname="argument secret_string_value", value=secret_string_value, expected_type=type_hints["secret_string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if generate_secret_string is not None:
            self._values["generate_secret_string"] = generate_secret_string
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replica_regions is not None:
            self._values["replica_regions"] = replica_regions
        if secret_name is not None:
            self._values["secret_name"] = secret_name
        if secret_string_beta1 is not None:
            self._values["secret_string_beta1"] = secret_string_beta1
        if secret_string_value is not None:
            self._values["secret_string_value"] = secret_string_value

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional, human-friendly description of the secret.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The customer-managed encryption key to use for encrypting the secret value.

        :default: - A default KMS key for the account and region is used.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def generate_secret_string(self) -> typing.Optional["SecretStringGenerator"]:
        '''(experimental) Configuration for how to generate a secret value.

        Only one of ``secretString`` and ``generateSecretString`` can be provided.

        :default:

        - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each
        category), per the default values of ``SecretStringGenerator``.

        :stability: experimental
        '''
        result = self._values.get("generate_secret_string")
        return typing.cast(typing.Optional["SecretStringGenerator"], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Policy to apply when the secret is removed from this stack.

        :default: - Not set.

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def replica_regions(self) -> typing.Optional[typing.List[ReplicaRegion]]:
        '''(experimental) A list of regions where to replicate this secret.

        :default: - Secret is not replicated

        :stability: experimental
        '''
        result = self._values.get("replica_regions")
        return typing.cast(typing.Optional[typing.List[ReplicaRegion]], result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the secret.

        Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to
        30 days blackout period. During that period, it is not possible to create another secret that shares the same name.

        :default: - A name is generated by CloudFormation.

        :stability: experimental
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_string_beta1(self) -> typing.Optional["SecretStringValueBeta1"]:
        '''(deprecated) Initial value for the secret.

        **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value.
        The secret string -- if provided -- will be included in the output of the cdk as part of synthesis,
        and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to
        another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access
        to the CloudFormation template (via the AWS Console, SDKs, or CLI).

        Specifies text data that you want to encrypt and store in this new version of the secret.
        May be a simple string value, or a string representation of a JSON structure.

        Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided.

        :default: - SecretsManager generates a new secret value.

        :deprecated: Use ``secretStringValue`` instead.

        :stability: deprecated
        '''
        result = self._values.get("secret_string_beta1")
        return typing.cast(typing.Optional["SecretStringValueBeta1"], result)

    @builtins.property
    def secret_string_value(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) Initial value for the secret.

        **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value.
        The secret string -- if provided -- will be included in the output of the cdk as part of synthesis,
        and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to
        another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access
        to the CloudFormation template (via the AWS Console, SDKs, or CLI).

        Specifies text data that you want to encrypt and store in this new version of the secret.
        May be a simple string value, or a string representation of a JSON structure.

        Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided.

        :default: - SecretsManager generates a new secret value.

        :stability: experimental
        '''
        result = self._values.get("secret_string_value")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretRotation(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.SecretRotation",
):
    '''(experimental) Secret rotation for a service or database.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_secret: secretsmanager.Secret
        # my_database: ec2.IConnectable
        # my_vpc: ec2.Vpc
        
        
        secretsmanager.SecretRotation(self, "SecretRotation",
            application=secretsmanager.SecretRotationApplication.MYSQL_ROTATION_SINGLE_USER,  # MySQL single user scheme
            secret=my_secret,
            target=my_database,  # a Connectable
            vpc=my_vpc,  # The VPC where the secret rotation application will be deployed
            exclude_characters=" %+:;{}"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application: "SecretRotationApplication",
        secret: ISecret,
        target: _IConnectable_c1c0e72c,
        vpc: _IVpc_6d1f76c4,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        endpoint: typing.Optional[_IInterfaceVpcEndpoint_6081623d] = None,
        exclude_characters: typing.Optional[builtins.str] = None,
        master_secret: typing.Optional[ISecret] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application: (experimental) The serverless application for the rotation.
        :param secret: (experimental) The secret to rotate. It must be a JSON string with the following format:. Example:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment`` or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        :param target: (experimental) The target service or database.
        :param vpc: (experimental) The VPC where the Lambda rotation function will run.
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param endpoint: (experimental) The VPC interface endpoint to use for the Secrets Manager API. If you enable private DNS hostnames for your VPC private endpoint (the default), you don't need to specify an endpoint. The standard Secrets Manager DNS hostname the Secrets Manager CLI and SDKs use by default (https://secretsmanager..amazonaws.com) automatically resolves to your VPC endpoint. Default: https://secretsmanager..amazonaws.com
        :param exclude_characters: (experimental) Characters which should not appear in the generated password. Default: - no additional characters are explicitly excluded
        :param master_secret: (experimental) The master secret for a multi user rotation scheme. Default: - single user rotation scheme
        :param security_group: (experimental) The security group for the Lambda rotation function. Default: - a new security group is created
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423d2411dce157331fb28215b3a1cef419cee98b9759b90c38af076e06727d2a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecretRotationProps(
            application=application,
            secret=secret,
            target=target,
            vpc=vpc,
            automatically_after=automatically_after,
            endpoint=endpoint,
            exclude_characters=exclude_characters,
            master_secret=master_secret,
            security_group=security_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class SecretRotationApplication(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.SecretRotationApplication",
):
    '''(experimental) A secret rotation serverless application.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_secret: secretsmanager.Secret
        # my_database: ec2.IConnectable
        # my_vpc: ec2.Vpc
        
        
        secretsmanager.SecretRotation(self, "SecretRotation",
            application=secretsmanager.SecretRotationApplication.MYSQL_ROTATION_SINGLE_USER,  # MySQL single user scheme
            secret=my_secret,
            target=my_database,  # a Connectable
            vpc=my_vpc,  # The VPC where the secret rotation application will be deployed
            exclude_characters=" %+:;{}"
        )
    '''

    def __init__(
        self,
        application_id: builtins.str,
        semantic_version: builtins.str,
        *,
        is_multi_user: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param application_id: -
        :param semantic_version: -
        :param is_multi_user: (experimental) Whether the rotation application uses the mutli user scheme. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594a14891a7de689b812116e880c1321f5841aeb7ab192b125b3d794e09fcca4)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument semantic_version", value=semantic_version, expected_type=type_hints["semantic_version"])
        options = SecretRotationApplicationOptions(is_multi_user=is_multi_user)

        jsii.create(self.__class__, self, [application_id, semantic_version, options])

    @jsii.member(jsii_name="applicationArnForPartition")
    def application_arn_for_partition(self, partition: builtins.str) -> builtins.str:
        '''(experimental) Returns the application ARN for the current partition.

        Can be used in combination with a ``CfnMapping`` to automatically select the correct ARN based on the current partition.

        :param partition: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63bc4ea1dc3d2725913ea7f973ac3c35746d8be26b0db14e7e4f00146d16858)
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
        return typing.cast(builtins.str, jsii.invoke(self, "applicationArnForPartition", [partition]))

    @jsii.member(jsii_name="semanticVersionForPartition")
    def semantic_version_for_partition(self, partition: builtins.str) -> builtins.str:
        '''(experimental) The semantic version of the app for the current partition.

        Can be used in combination with a ``CfnMapping`` to automatically select the correct version based on the current partition.

        :param partition: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ae91a5d1694c69737f871316a3fe29629fef99e95451c19b8dc88ef8bcd212)
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
        return typing.cast(builtins.str, jsii.invoke(self, "semanticVersionForPartition", [partition]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MARIADB_ROTATION_MULTI_USER")
    def MARIADB_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS MariaDB using the multi user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "MARIADB_ROTATION_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MARIADB_ROTATION_SINGLE_USER")
    def MARIADB_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS MariaDB using the single user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "MARIADB_ROTATION_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONGODB_ROTATION_MULTI_USER")
    def MONGODB_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for MongoDB using the multi user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "MONGODB_ROTATION_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONGODB_ROTATION_SINGLE_USER")
    def MONGODB_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for MongoDB using the single user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "MONGODB_ROTATION_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MYSQL_ROTATION_MULTI_USER")
    def MYSQL_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS MySQL using the multi user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "MYSQL_ROTATION_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MYSQL_ROTATION_SINGLE_USER")
    def MYSQL_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS MySQL using the single user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "MYSQL_ROTATION_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_ROTATION_MULTI_USER")
    def ORACLE_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS Oracle using the multi user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "ORACLE_ROTATION_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_ROTATION_SINGLE_USER")
    def ORACLE_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS Oracle using the single user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "ORACLE_ROTATION_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="POSTGRES_ROTATION_MULTI_USER")
    def POSTGRES_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS PostgreSQL using the multi user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "POSTGRES_ROTATION_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="POSTGRES_ROTATION_SINGLE_USER")
    def POSTGRES_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS PostgreSQL using the single user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "POSTGRES_ROTATION_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDSHIFT_ROTATION_MULTI_USER")
    def REDSHIFT_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for Amazon Redshift using the multi user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "REDSHIFT_ROTATION_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDSHIFT_ROTATION_SINGLE_USER")
    def REDSHIFT_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for Amazon Redshift using the single user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "REDSHIFT_ROTATION_SINGLE_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQLSERVER_ROTATION_MULTI_USER")
    def SQLSERVER_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS SQL Server using the multi user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "SQLSERVER_ROTATION_MULTI_USER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQLSERVER_ROTATION_SINGLE_USER")
    def SQLSERVER_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        '''(experimental) Conducts an AWS SecretsManager secret rotation for RDS SQL Server using the single user rotation scheme.

        :stability: experimental
        '''
        return typing.cast("SecretRotationApplication", jsii.sget(cls, "SQLSERVER_ROTATION_SINGLE_USER"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''(deprecated) The application identifier of the rotation application.

        :deprecated: only valid when deploying to the 'aws' partition. Use ``applicationArnForPartition`` instead.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @builtins.property
    @jsii.member(jsii_name="semanticVersion")
    def semantic_version(self) -> builtins.str:
        '''(deprecated) The semantic version of the rotation application.

        :deprecated: only valid when deploying to the 'aws' partition. Use ``semanticVersionForPartition`` instead.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "semanticVersion"))

    @builtins.property
    @jsii.member(jsii_name="isMultiUser")
    def is_multi_user(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the rotation application uses the mutli user scheme.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "isMultiUser"))


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.SecretRotationApplicationOptions",
    jsii_struct_bases=[],
    name_mapping={"is_multi_user": "isMultiUser"},
)
class SecretRotationApplicationOptions:
    def __init__(self, *, is_multi_user: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options for a SecretRotationApplication.

        :param is_multi_user: (experimental) Whether the rotation application uses the mutli user scheme. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            secret_rotation_application_options = secretsmanager.SecretRotationApplicationOptions(
                is_multi_user=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058a3fa715cfdfddf30097b695be9ce238c8deaa53f1f6dffa8f1dc5710c9872)
            check_type(argname="argument is_multi_user", value=is_multi_user, expected_type=type_hints["is_multi_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_multi_user is not None:
            self._values["is_multi_user"] = is_multi_user

    @builtins.property
    def is_multi_user(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the rotation application uses the mutli user scheme.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("is_multi_user")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretRotationApplicationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.SecretRotationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "secret": "secret",
        "target": "target",
        "vpc": "vpc",
        "automatically_after": "automaticallyAfter",
        "endpoint": "endpoint",
        "exclude_characters": "excludeCharacters",
        "master_secret": "masterSecret",
        "security_group": "securityGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class SecretRotationProps:
    def __init__(
        self,
        *,
        application: SecretRotationApplication,
        secret: ISecret,
        target: _IConnectable_c1c0e72c,
        vpc: _IVpc_6d1f76c4,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        endpoint: typing.Optional[_IInterfaceVpcEndpoint_6081623d] = None,
        exclude_characters: typing.Optional[builtins.str] = None,
        master_secret: typing.Optional[ISecret] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Construction properties for a SecretRotation.

        :param application: (experimental) The serverless application for the rotation.
        :param secret: (experimental) The secret to rotate. It must be a JSON string with the following format:. Example:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment`` or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        :param target: (experimental) The target service or database.
        :param vpc: (experimental) The VPC where the Lambda rotation function will run.
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param endpoint: (experimental) The VPC interface endpoint to use for the Secrets Manager API. If you enable private DNS hostnames for your VPC private endpoint (the default), you don't need to specify an endpoint. The standard Secrets Manager DNS hostname the Secrets Manager CLI and SDKs use by default (https://secretsmanager..amazonaws.com) automatically resolves to your VPC endpoint. Default: https://secretsmanager..amazonaws.com
        :param exclude_characters: (experimental) Characters which should not appear in the generated password. Default: - no additional characters are explicitly excluded
        :param master_secret: (experimental) The master secret for a multi user rotation scheme. Default: - single user rotation scheme
        :param security_group: (experimental) The security group for the Lambda rotation function. Default: - a new security group is created
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_secret: secretsmanager.Secret
            # my_database: ec2.IConnectable
            # my_vpc: ec2.Vpc
            
            
            secretsmanager.SecretRotation(self, "SecretRotation",
                application=secretsmanager.SecretRotationApplication.MYSQL_ROTATION_SINGLE_USER,  # MySQL single user scheme
                secret=my_secret,
                target=my_database,  # a Connectable
                vpc=my_vpc,  # The VPC where the secret rotation application will be deployed
                exclude_characters=" %+:;{}"
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ecbf9b6283a782d394b1b5ad30923f987015002920b300a30d0a5af38cf01bf)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument automatically_after", value=automatically_after, expected_type=type_hints["automatically_after"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument exclude_characters", value=exclude_characters, expected_type=type_hints["exclude_characters"])
            check_type(argname="argument master_secret", value=master_secret, expected_type=type_hints["master_secret"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application": application,
            "secret": secret,
            "target": target,
            "vpc": vpc,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if exclude_characters is not None:
            self._values["exclude_characters"] = exclude_characters
        if master_secret is not None:
            self._values["master_secret"] = master_secret
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def application(self) -> SecretRotationApplication:
        '''(experimental) The serverless application for the rotation.

        :stability: experimental
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(SecretRotationApplication, result)

    @builtins.property
    def secret(self) -> ISecret:
        '''(experimental) The secret to rotate. It must be a JSON string with the following format:.

        Example::

           {
              "engine": <required: database engine>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port will be used>,
              "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords>
           }

        This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment``
        or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
        :stability: experimental
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(ISecret, result)

    @builtins.property
    def target(self) -> _IConnectable_c1c0e72c:
        '''(experimental) The target service or database.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(_IConnectable_c1c0e72c, result)

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) The VPC where the Lambda rotation function will run.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        :default: Duration.days(30)

        :stability: experimental
        '''
        result = self._values.get("automatically_after")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[_IInterfaceVpcEndpoint_6081623d]:
        '''(experimental) The VPC interface endpoint to use for the Secrets Manager API.

        If you enable private DNS hostnames for your VPC private endpoint (the default), you don't
        need to specify an endpoint. The standard Secrets Manager DNS hostname the Secrets Manager
        CLI and SDKs use by default (https://secretsmanager..amazonaws.com) automatically
        resolves to your VPC endpoint.

        :default: https://secretsmanager..amazonaws.com

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[_IInterfaceVpcEndpoint_6081623d], result)

    @builtins.property
    def exclude_characters(self) -> typing.Optional[builtins.str]:
        '''(experimental) Characters which should not appear in the generated password.

        :default: - no additional characters are explicitly excluded

        :stability: experimental
        '''
        result = self._values.get("exclude_characters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_secret(self) -> typing.Optional[ISecret]:
        '''(experimental) The master secret for a multi user rotation scheme.

        :default: - single user rotation scheme

        :stability: experimental
        '''
        result = self._values.get("master_secret")
        return typing.cast(typing.Optional[ISecret], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(experimental) The security group for the Lambda rotation function.

        :default: - a new security group is created

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) The type of subnets in the VPC where the Lambda rotation function will run.

        :default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretRotationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.SecretStringGenerator",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_characters": "excludeCharacters",
        "exclude_lowercase": "excludeLowercase",
        "exclude_numbers": "excludeNumbers",
        "exclude_punctuation": "excludePunctuation",
        "exclude_uppercase": "excludeUppercase",
        "generate_string_key": "generateStringKey",
        "include_space": "includeSpace",
        "password_length": "passwordLength",
        "require_each_included_type": "requireEachIncludedType",
        "secret_string_template": "secretStringTemplate",
    },
)
class SecretStringGenerator:
    def __init__(
        self,
        *,
        exclude_characters: typing.Optional[builtins.str] = None,
        exclude_lowercase: typing.Optional[builtins.bool] = None,
        exclude_numbers: typing.Optional[builtins.bool] = None,
        exclude_punctuation: typing.Optional[builtins.bool] = None,
        exclude_uppercase: typing.Optional[builtins.bool] = None,
        generate_string_key: typing.Optional[builtins.str] = None,
        include_space: typing.Optional[builtins.bool] = None,
        password_length: typing.Optional[jsii.Number] = None,
        require_each_included_type: typing.Optional[builtins.bool] = None,
        secret_string_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration to generate secrets such as passwords automatically.

        :param exclude_characters: (experimental) A string that includes characters that shouldn't be included in the generated password. The string can be a minimum of ``0`` and a maximum of ``4096`` characters long. Default: no exclusions
        :param exclude_lowercase: (experimental) Specifies that the generated password shouldn't include lowercase letters. Default: false
        :param exclude_numbers: (experimental) Specifies that the generated password shouldn't include digits. Default: false
        :param exclude_punctuation: (experimental) Specifies that the generated password shouldn't include punctuation characters. Default: false
        :param exclude_uppercase: (experimental) Specifies that the generated password shouldn't include uppercase letters. Default: false
        :param generate_string_key: (experimental) The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter. If you specify ``generateStringKey`` then ``secretStringTemplate`` must be also be specified.
        :param include_space: (experimental) Specifies that the generated password can include the space character. Default: false
        :param password_length: (experimental) The desired length of the generated password. Default: 32
        :param require_each_included_type: (experimental) Specifies whether the generated password must include at least one of every allowed character type. Default: true
        :param secret_string_template: (experimental) A properly structured JSON string that the generated password can be added to. The ``generateStringKey`` is combined with the generated random string and inserted into the JSON structure that's specified by this parameter. The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate`` then ``generateStringKey`` must be also be specified.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Default secret
            secret = secretsmanager.Secret(self, "Secret")
            # Using the default secret
            iam.User(self, "User",
                password=secret.secret_value
            )
            # Templated secret
            templated_secret = secretsmanager.Secret(self, "TemplatedSecret",
                generate_secret_string=secretsmanager.aws_secretsmanager.SecretStringGenerator(
                    secret_string_template=JSON.stringify({"username": "user"}),
                    generate_string_key="password"
                )
            )
            # Using the templated secret
            iam.User(self, "OtherUser",
                user_name=templated_secret.secret_value_from_json("username").to_string(),
                password=templated_secret.secret_value_from_json("password")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae31eacb8896a374a5c4f7ba3e3e45625413cba87b97055e209cc9519f745118)
            check_type(argname="argument exclude_characters", value=exclude_characters, expected_type=type_hints["exclude_characters"])
            check_type(argname="argument exclude_lowercase", value=exclude_lowercase, expected_type=type_hints["exclude_lowercase"])
            check_type(argname="argument exclude_numbers", value=exclude_numbers, expected_type=type_hints["exclude_numbers"])
            check_type(argname="argument exclude_punctuation", value=exclude_punctuation, expected_type=type_hints["exclude_punctuation"])
            check_type(argname="argument exclude_uppercase", value=exclude_uppercase, expected_type=type_hints["exclude_uppercase"])
            check_type(argname="argument generate_string_key", value=generate_string_key, expected_type=type_hints["generate_string_key"])
            check_type(argname="argument include_space", value=include_space, expected_type=type_hints["include_space"])
            check_type(argname="argument password_length", value=password_length, expected_type=type_hints["password_length"])
            check_type(argname="argument require_each_included_type", value=require_each_included_type, expected_type=type_hints["require_each_included_type"])
            check_type(argname="argument secret_string_template", value=secret_string_template, expected_type=type_hints["secret_string_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_characters is not None:
            self._values["exclude_characters"] = exclude_characters
        if exclude_lowercase is not None:
            self._values["exclude_lowercase"] = exclude_lowercase
        if exclude_numbers is not None:
            self._values["exclude_numbers"] = exclude_numbers
        if exclude_punctuation is not None:
            self._values["exclude_punctuation"] = exclude_punctuation
        if exclude_uppercase is not None:
            self._values["exclude_uppercase"] = exclude_uppercase
        if generate_string_key is not None:
            self._values["generate_string_key"] = generate_string_key
        if include_space is not None:
            self._values["include_space"] = include_space
        if password_length is not None:
            self._values["password_length"] = password_length
        if require_each_included_type is not None:
            self._values["require_each_included_type"] = require_each_included_type
        if secret_string_template is not None:
            self._values["secret_string_template"] = secret_string_template

    @builtins.property
    def exclude_characters(self) -> typing.Optional[builtins.str]:
        '''(experimental) A string that includes characters that shouldn't be included in the generated password.

        The string can be a minimum
        of ``0`` and a maximum of ``4096`` characters long.

        :default: no exclusions

        :stability: experimental
        '''
        result = self._values.get("exclude_characters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_lowercase(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies that the generated password shouldn't include lowercase letters.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("exclude_lowercase")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exclude_numbers(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies that the generated password shouldn't include digits.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("exclude_numbers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exclude_punctuation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies that the generated password shouldn't include punctuation characters.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("exclude_punctuation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exclude_uppercase(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies that the generated password shouldn't include uppercase letters.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("exclude_uppercase")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def generate_string_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter.

        If you specify ``generateStringKey`` then ``secretStringTemplate``
        must be also be specified.

        :stability: experimental
        '''
        result = self._values.get("generate_string_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_space(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies that the generated password can include the space character.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("include_space")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def password_length(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The desired length of the generated password.

        :default: 32

        :stability: experimental
        '''
        result = self._values.get("password_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_each_included_type(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the generated password must include at least one of every allowed character type.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("require_each_included_type")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secret_string_template(self) -> typing.Optional[builtins.str]:
        '''(experimental) A properly structured JSON string that the generated password can be added to.

        The ``generateStringKey`` is
        combined with the generated random string and inserted into the JSON structure that's specified by this parameter.
        The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate``
        then ``generateStringKey`` must be also be specified.

        :stability: experimental
        '''
        result = self._values.get("secret_string_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretStringGenerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretStringValueBeta1(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.SecretStringValueBeta1",
):
    '''(deprecated) An experimental class used to specify an initial secret value for a Secret.

    The class wraps a simple string (or JSON representation) in order to provide some safety checks and warnings
    about the dangers of using plaintext strings as initial secret seed values via CDK/CloudFormation.

    :deprecated: Use ``cdk.SecretValue`` instead.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        # Creates a new IAM user, access and secret keys, and stores the secret access key in a Secret.
        user = iam.User(self, "User")
        access_key = iam.AccessKey(self, "AccessKey", user=user)
        secret_value = secretsmanager.SecretStringValueBeta1.from_token(access_key.secret_access_key.to_string())
        secretsmanager.Secret(self, "Secret",
            secret_string_beta1=secret_value
        )
    '''

    @jsii.member(jsii_name="fromToken")
    @builtins.classmethod
    def from_token(
        cls,
        secret_value_from_token: builtins.str,
    ) -> "SecretStringValueBeta1":
        '''(deprecated) Creates a ``SecretValueValueBeta1`` from a string value coming from a Token.

        The intent is to enable creating secrets from references (e.g., ``Ref``, ``Fn::GetAtt``) from other resources.
        This might be the direct output of another Construct, or the output of a Custom Resource.
        This method throws if it determines the input is an unsafe plaintext string.

        For example::

           # Creates a new IAM user, access and secret keys, and stores the secret access key in a Secret.
           user = iam.User(self, "User")
           access_key = iam.AccessKey(self, "AccessKey", user=user)
           secret_value = secretsmanager.SecretStringValueBeta1.from_token(access_key.secret_access_key.to_string())
           secretsmanager.Secret(self, "Secret",
               secret_string_beta1=secret_value
           )

        The secret may also be embedded in a string representation of a JSON structure::

           user = iam.User(self, "User")
           access_key = iam.AccessKey(self, "AccessKey", user=user)
           secret_value = secretsmanager.SecretStringValueBeta1.from_token(JSON.stringify({
               "username": user.user_name,
               "database": "foo",
               "password": access_key.secret_access_key.unsafe_unwrap()
           }))

        Note that the value being a Token does *not* guarantee safety. For example, a Lazy-evaluated string
        (e.g., ``Lazy.string({ produce: () => 'myInsecurePassword' }))``) is a Token, but as the output is
        ultimately a plaintext string, and so insecure.

        :param secret_value_from_token: a secret value coming from a Construct attribute or Custom Resource output.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d8e8c1bd7e931e7d9b69de30b3bc72eb4f52fa8b6344727f6ec727c99287d3)
            check_type(argname="argument secret_value_from_token", value=secret_value_from_token, expected_type=type_hints["secret_value_from_token"])
        return typing.cast("SecretStringValueBeta1", jsii.sinvoke(cls, "fromToken", [secret_value_from_token]))

    @jsii.member(jsii_name="fromUnsafePlaintext")
    @builtins.classmethod
    def from_unsafe_plaintext(
        cls,
        secret_value: builtins.str,
    ) -> "SecretStringValueBeta1":
        '''(deprecated) Creates a ``SecretStringValueBeta1`` from a plaintext value.

        This approach is inherently unsafe, as the secret value may be visible in your source control repository
        and will also appear in plaintext in the resulting CloudFormation template, including in the AWS Console or APIs.
        Usage of this method is discouraged, especially for production workloads.

        :param secret_value: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b8dbe810d3cec9f1b48dae765ed2ad2d7ae32399531d8640bf3b9c4daa622a)
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
        return typing.cast("SecretStringValueBeta1", jsii.sinvoke(cls, "fromUnsafePlaintext", [secret_value]))

    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> builtins.str:
        '''(deprecated) Returns the secret value.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "secretValue", []))


@jsii.implements(ISecretTargetAttachment, ISecret)
class SecretTargetAttachment(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_secretsmanager.SecretTargetAttachment",
):
    '''(experimental) An attached secret.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_secretsmanager as secretsmanager
        
        # secret: secretsmanager.Secret
        # secret_attachment_target: secretsmanager.ISecretAttachmentTarget
        
        secret_target_attachment = secretsmanager.SecretTargetAttachment(self, "MySecretTargetAttachment",
            secret=secret,
            target=secret_attachment_target
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        secret: ISecret,
        target: ISecretAttachmentTarget,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param secret: (experimental) The secret to attach to the target.
        :param target: (experimental) The target to attach the secret to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d3b241d255f86705eac855bdbc7082c0c0e434c10833ac31dfa08470523763)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecretTargetAttachmentProps(secret=secret, target=target)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretTargetAttachmentSecretArn")
    @builtins.classmethod
    def from_secret_target_attachment_secret_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        secret_target_attachment_secret_arn: builtins.str,
    ) -> ISecretTargetAttachment:
        '''
        :param scope: -
        :param id: -
        :param secret_target_attachment_secret_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e6ce24cf4089a0ea86dc94dcf3080b56487b9c745f8c98f453273583cbc1c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret_target_attachment_secret_arn", value=secret_target_attachment_secret_arn, expected_type=type_hints["secret_target_attachment_secret_arn"])
        return typing.cast(ISecretTargetAttachment, jsii.sinvoke(cls, "fromSecretTargetAttachmentSecretArn", [scope, id, secret_target_attachment_secret_arn]))

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
    ) -> RotationSchedule:
        '''(experimental) Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. A value of zero will disable automatic rotation - ``Duration.days(0)``. Default: Duration.days(30)
        :param hosted_rotation: (experimental) Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: (experimental) A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95e4852f0780735c90d1df0cd3f363dc33c51cd8eec636292041fa94cb823ca)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = RotationScheduleOptions(
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotation_lambda=rotation_lambda,
        )

        return typing.cast(RotationSchedule, jsii.invoke(self, "addRotationSchedule", [id, options]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93ea749b256c79a037c98ce9c2bf410c159bcb56c1fddb9e5adc0fb5479ef9a)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="attach")
    def attach(self, target: ISecretAttachmentTarget) -> ISecret:
        '''(experimental) Attach a target to this secret.

        :param target: The target to attach.

        :return: An attached secret

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6c9f08b1ed49815f5849cbb7a04a776b8137219a98b771bfe2626d9758ae351)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(ISecret, jsii.invoke(self, "attach", [target]))

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        '''(experimental) Denies the ``DeleteSecret`` action to all principals within the current account.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "denyAccountRootDelete", []))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_4c5a91d1,
        version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03199f5be15ce79d1809e9c0c666fa3b534ab5d6281c680555a279f5926d7899)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument version_stages", value=version_stages, expected_type=type_hints["version_stages"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee, version_stages]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants writing and updating the secret value to some role.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafb6c5caf6611af25f5be67ba91bb8aa23d35c64cc67da8e975cb121aa96bb5)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, json_field: builtins.str) -> _SecretValue_c18506ef:
        '''(experimental) Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d00a65b80dfdb60f8730dcdc9c990e0772af83287970478dfee72d271f0bfaa)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast(_SecretValue_c18506ef, jsii.invoke(self, "secretValueFromJson", [json_field]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="arnForPolicies")
    def _arn_for_policies(self) -> builtins.str:
        '''(experimental) Provides an identifier for this secret for use in IAM policies.

        If there is a full ARN, this is just the ARN;
        if we have a partial ARN -- due to either importing by secret name or partial ARN --
        then we need to add a suffix to capture the full ARN's format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arnForPolicies"))

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        '''(experimental) The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        '''(experimental) The name of the secret.

        For "owned" secrets, this will be the full resource name (secret name + suffix), unless the
        '@aws-cdk/aws-secretsmanager:parseOwnedSecretName' feature flag is set.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @builtins.property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> builtins.str:
        '''(experimental) Same as ``secretArn``.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretTargetAttachmentSecretArn"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _SecretValue_c18506ef:
        '''(experimental) Retrieve the value of the stored secret as a ``SecretValue``.

        :stability: experimental
        '''
        return typing.cast(_SecretValue_c18506ef, jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretFullArn"))


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.SecretTargetAttachmentProps",
    jsii_struct_bases=[AttachedSecretOptions],
    name_mapping={"target": "target", "secret": "secret"},
)
class SecretTargetAttachmentProps(AttachedSecretOptions):
    def __init__(self, *, target: ISecretAttachmentTarget, secret: ISecret) -> None:
        '''(experimental) Construction properties for an AttachedSecret.

        :param target: (experimental) The target to attach the secret to.
        :param secret: (experimental) The secret to attach to the target.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_secretsmanager as secretsmanager
            
            # secret: secretsmanager.Secret
            # secret_attachment_target: secretsmanager.ISecretAttachmentTarget
            
            secret_target_attachment_props = secretsmanager.SecretTargetAttachmentProps(
                secret=secret,
                target=secret_attachment_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e1a9642f84a68ab4c0d68ef8d2f5554324d0201a754ee0f383488417a70210)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "secret": secret,
        }

    @builtins.property
    def target(self) -> ISecretAttachmentTarget:
        '''(experimental) The target to attach the secret to.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(ISecretAttachmentTarget, result)

    @builtins.property
    def secret(self) -> ISecret:
        '''(experimental) The secret to attach to the target.

        :stability: experimental
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretTargetAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.SingleUserHostedRotationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "security_groups": "securityGroups",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class SingleUserHostedRotationOptions:
    def __init__(
        self,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Single user hosted rotation options.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_vpc: ec2.Vpc
            # db_connections: ec2.Connections
            # secret: secretsmanager.Secret
            
            
            my_hosted_rotation = secretsmanager.HostedRotation.mysql_single_user(vpc=my_vpc)
            secret.add_rotation_schedule("RotationSchedule", hosted_rotation=my_hosted_rotation)
            db_connections.allow_default_port_from(my_hosted_rotation)
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e225d2ecd116440be1e79d9a19262707b2eb913aca927415f45b7d0bd8ecb1)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if function_name is not None:
            self._values["function_name"] = function_name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the Lambda created to rotate the secret.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) A list of security groups for the Lambda created to rotate the secret.

        :default: - a new security group is created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where the Lambda rotation function will run.

        :default: - the Lambda is not deployed in a VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) The type of subnets in the VPC where the Lambda rotation function will run.

        :default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SingleUserHostedRotationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_secretsmanager.MultiUserHostedRotationOptions",
    jsii_struct_bases=[SingleUserHostedRotationOptions],
    name_mapping={
        "function_name": "functionName",
        "security_groups": "securityGroups",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "master_secret": "masterSecret",
    },
)
class MultiUserHostedRotationOptions(SingleUserHostedRotationOptions):
    def __init__(
        self,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        master_secret: ISecret,
    ) -> None:
        '''(experimental) Multi user hosted rotation options.

        :param function_name: (experimental) A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: (experimental) A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: (experimental) The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: (experimental) The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        :param master_secret: (experimental) The master secret for a multi user rotation scheme.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_ec2 as ec2
            from monocdk import aws_secretsmanager as secretsmanager
            
            # secret: secretsmanager.Secret
            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # vpc: ec2.Vpc
            
            multi_user_hosted_rotation_options = secretsmanager.MultiUserHostedRotationOptions(
                master_secret=secret,
            
                # the properties below are optional
                function_name="functionName",
                security_groups=[security_group],
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnet_name="subnetName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.ISOLATED
                )
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc5360b033a9c70b6d2aaaee0b11f630f889961325760c8372a625ed3a927ed)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument master_secret", value=master_secret, expected_type=type_hints["master_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "master_secret": master_secret,
        }
        if function_name is not None:
            self._values["function_name"] = function_name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the Lambda created to rotate the secret.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) A list of security groups for the Lambda created to rotate the secret.

        :default: - a new security group is created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where the Lambda rotation function will run.

        :default: - the Lambda is not deployed in a VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) The type of subnets in the VPC where the Lambda rotation function will run.

        :default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def master_secret(self) -> ISecret:
        '''(experimental) The master secret for a multi user rotation scheme.

        :stability: experimental
        '''
        result = self._values.get("master_secret")
        assert result is not None, "Required property 'master_secret' is missing"
        return typing.cast(ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultiUserHostedRotationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AttachedSecretOptions",
    "AttachmentTargetType",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
    "CfnRotationSchedule",
    "CfnRotationScheduleProps",
    "CfnSecret",
    "CfnSecretProps",
    "CfnSecretTargetAttachment",
    "CfnSecretTargetAttachmentProps",
    "HostedRotation",
    "HostedRotationType",
    "ISecret",
    "ISecretAttachmentTarget",
    "ISecretTargetAttachment",
    "MultiUserHostedRotationOptions",
    "ReplicaRegion",
    "ResourcePolicy",
    "ResourcePolicyProps",
    "RotationSchedule",
    "RotationScheduleOptions",
    "RotationScheduleProps",
    "Secret",
    "SecretAttachmentTargetProps",
    "SecretAttributes",
    "SecretProps",
    "SecretRotation",
    "SecretRotationApplication",
    "SecretRotationApplicationOptions",
    "SecretRotationProps",
    "SecretStringGenerator",
    "SecretStringValueBeta1",
    "SecretTargetAttachment",
    "SecretTargetAttachmentProps",
    "SingleUserHostedRotationOptions",
]

publication.publish()

def _typecheckingstub__4fc9e7a1d3cbbf406c3cf36e9155ecf967fd10750a8fea967ea8ffab53e86565(
    *,
    target: ISecretAttachmentTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e150ea28ef4b0f25a0eef706af436d1e3482033b921cb723167aa8f6b1d75739(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    resource_policy: typing.Any,
    secret_id: builtins.str,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea43da867688023566a0be83c5f82c9691b0ad05ec09a14692965ccd667984e1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd41eee94e0284d231384addb9acfa7724515d1eb5d445c7bc70036fbd77c39(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc990d92d95299d84354eb546c8320628b7b8328ec3314bbe11662e7360adcef(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0c2613fd8951e4f86ce669e1bc45b3b79d015edc0fa6e926544dd75e682ab0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf5214200e72ff19db4afea8dc3e9bf2b9b199dca5b196fb7ca8d76d1bfea79(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f2a968037f043ebc0e399ed715cb98a161407eee89ad77829aa8e9abaefca5(
    *,
    resource_policy: typing.Any,
    secret_id: builtins.str,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b05e81d2584648f9ee8606b4d8692ac1107eff30872855d7c6cb3cbbcfa10a1(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    secret_id: builtins.str,
    hosted_rotation_lambda: typing.Optional[typing.Union[typing.Union[CfnRotationSchedule.HostedRotationLambdaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rotate_immediately_on_update: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    rotation_lambda_arn: typing.Optional[builtins.str] = None,
    rotation_rules: typing.Optional[typing.Union[typing.Union[CfnRotationSchedule.RotationRulesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f638a0ec15bde8dc2b468d1c204a08641561580102589c8e8cbfbee892a51a6a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa44e940b824df54ce4a81fb1a84e098cf7c77005251371ac915f11accd6a065(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f370d4c3ad544299de955b56a01d31094df5799510865b65bbd972ddec42f4a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5674db8b9f3df6c9bffa8fbeb215204b32874e4cbf3cacac2e883aba54b563b(
    value: typing.Optional[typing.Union[CfnRotationSchedule.HostedRotationLambdaProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44719747806e5a20dfa5bc090319856defe011e532d9a35e0d971d81520fcbc1(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3edecee3376a880267fe46d4314bcda32e33f70e64000766bcf36ee0ba32a0e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6cdc07df79420ebc4b70d2c20585eb33118bb7f876f8bed5e9f7902ba35a0b(
    value: typing.Optional[typing.Union[CfnRotationSchedule.RotationRulesProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21cca99480caf5adc27fdc5bbf0f89705819515be41087372db6f9b977b8044(
    *,
    rotation_type: builtins.str,
    exclude_characters: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    master_secret_arn: typing.Optional[builtins.str] = None,
    master_secret_kms_key_arn: typing.Optional[builtins.str] = None,
    rotation_lambda_name: typing.Optional[builtins.str] = None,
    superuser_secret_arn: typing.Optional[builtins.str] = None,
    superuser_secret_kms_key_arn: typing.Optional[builtins.str] = None,
    vpc_security_group_ids: typing.Optional[builtins.str] = None,
    vpc_subnet_ids: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af032eee28276438badaf1898ba41bce18eb796ae654f2d7239b5397f96e4ca7(
    *,
    automatically_after_days: typing.Optional[jsii.Number] = None,
    duration: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee97b74cc1d45e9e48f06df1f73390ea9a6584614534e1f4f3ea666f4830d69(
    *,
    secret_id: builtins.str,
    hosted_rotation_lambda: typing.Optional[typing.Union[typing.Union[CfnRotationSchedule.HostedRotationLambdaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rotate_immediately_on_update: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    rotation_lambda_arn: typing.Optional[builtins.str] = None,
    rotation_rules: typing.Optional[typing.Union[typing.Union[CfnRotationSchedule.RotationRulesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e1150daf1664acc1182e989d5df4fba0ab6e0a84f83086637b4df790b74f93(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    generate_secret_string: typing.Optional[typing.Union[typing.Union[CfnSecret.GenerateSecretStringProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    replica_regions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSecret.ReplicaRegionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    secret_string: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d2977b221cc0094de62190cd9c7776223cacd8c1451efc2a80958047fe8446(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590f95da6aefde77dee3040ecaf45cbac54a2d8267737cefcbf6e0f8540acdaa(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d250ba407e5e4bf985dc9770e5bcdc6fa1481feb04757fa42a924ee68d7bfb62(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6239caa307d8062a5c61bb36b6122bc7ed08512ca441a98da03b62e91fe74d05(
    value: typing.Optional[typing.Union[CfnSecret.GenerateSecretStringProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6dc1f75fc7fa7ce0c2d225bc315a54fd0bd9bd9ddea9c5fd9917f277abf0186(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b9fcbacdab823c3e3e122bc2d2c03afce669a172f5b6aad05023056a06550b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2563a98b30aab3cde3787db85a2a8125a48e12191fb1d39b28837e171a1be364(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSecret.ReplicaRegionProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e219663b233e1359842bf37fde5846c36b5595df0b4e2fb6b5e11cef868797(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a6d449671a19ac5f72658c5f15bccdea8c610490498bf347b7c2ccd48da9b4(
    *,
    exclude_characters: typing.Optional[builtins.str] = None,
    exclude_lowercase: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    exclude_numbers: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    exclude_punctuation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    exclude_uppercase: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    generate_string_key: typing.Optional[builtins.str] = None,
    include_space: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    password_length: typing.Optional[jsii.Number] = None,
    require_each_included_type: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    secret_string_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63288429b6aeb267cec681ce097a093d94edc0799ccfa68a089c2e0be35d3b7(
    *,
    region: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6800cd79b70824bb85a0a168d974da6297709622676ea47f0d6f6ef74ce1f99(
    *,
    description: typing.Optional[builtins.str] = None,
    generate_secret_string: typing.Optional[typing.Union[typing.Union[CfnSecret.GenerateSecretStringProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    replica_regions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSecret.ReplicaRegionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    secret_string: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227308d12a64af3b37b061d81d303772e178f78cfedb822e6311a75e3cf90677(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    secret_id: builtins.str,
    target_id: builtins.str,
    target_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f061fb1a3be887a3976c628757eafb259a6880e85c5f4a72b7dfdaaa275f9f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0feae507db7721704a3c909aac4856c7c29d0680abb1f0d824a9f86f61e12241(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d13b1cc0b7649bcd4b5031cf2fda6fa94302d0c79d17e324394439aac19ec54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a163dcb6948283ee242a198eeb575a4dacc984e12d022c47790ef0a29edc5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc25b3a55c83c5ba0eb20565f36a37aaa66012b0b80fa8ad1541c695cab40512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c88e52141ebf2a6f7f26db037bf2076dd15a802934aa41047355654578d339(
    *,
    secret_id: builtins.str,
    target_id: builtins.str,
    target_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332e05edcf7cc25bd609fd447457c936c1f719460c14bd94c95935fe997f43b3(
    secret: ISecret,
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c584027a331b568c5553ab4136dc8cddb26dd42bf6e60c5d4607eaec8f7e29(
    id: builtins.str,
    *,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
    hosted_rotation: typing.Optional[HostedRotation] = None,
    rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e602c2044eca7da229fd242caf9dd48b37ab8a4498d2994b097db577791940(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8b8471522fdf309d1f5a6e4c15400bbf8fbdff2fe60649bdfca327a38b55e6(
    target: ISecretAttachmentTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9341fe8876da08f94c51ab1668554157b497f515f319ef17cc48c47ec8aef15(
    grantee: _IGrantable_4c5a91d1,
    version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e2ea86c5a628690e3f8078d34a08bf0735701c3b123ff5db4f59a89a5e2ce0(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75485d103556923a9b50675ac451df40995da778166f60ccb4d53820c0bb11c(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e512691cba43679c69de55ff880e526f2584caf492dbd7a621846a83ecd5a1ce(
    *,
    region: builtins.str,
    encryption_key: typing.Optional[_IKey_36930160] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70938f171b6277261bcee1645321cafa60b767cf3fd1bda370a98172b7a21990(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    secret: ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393ff0d8d30f68e45e20ef7d14b5b51362f8777d9c921bc1ad3f079600eaba23(
    *,
    secret: ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01eef254b517f86b64586d47c9ddca0f881d46b9fbbeaee902e8f9773769c251(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    secret: ISecret,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
    hosted_rotation: typing.Optional[HostedRotation] = None,
    rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6388f2e710db296a0664f7bf706e1434418e796cf2b17eb289ede17b724d8406(
    *,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
    hosted_rotation: typing.Optional[HostedRotation] = None,
    rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68355b16e6fca2935627847eb7b24318773346d156160bf5faa72c09ad87ab4(
    *,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
    hosted_rotation: typing.Optional[HostedRotation] = None,
    rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
    secret: ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581e1f4f899e23c37781d58022f68e6e049ce0863aba6b4751cfa3a3c0e4e40e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    generate_secret_string: typing.Optional[typing.Union[SecretStringGenerator, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    replica_regions: typing.Optional[typing.Sequence[typing.Union[ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_name: typing.Optional[builtins.str] = None,
    secret_string_beta1: typing.Optional[SecretStringValueBeta1] = None,
    secret_string_value: typing.Optional[_SecretValue_c18506ef] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2550fba972082faed970e015a6121ae691fdd098fe490ab39845303c56a0a3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9238662dcf167408b8efa17536971f09089e40a5f3c0b2575446d908ff4b69e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    secret_complete_arn: typing.Optional[builtins.str] = None,
    secret_partial_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9719bccc2c68509dd77d173bf0bf86686a759ce199549812aa59043b25a2d1f2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    secret_complete_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e5304ba8babbcca0bcc0b1df44e50656db70a1c86599ed01b64b2098145dc2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd50dc99b2558e5c0c9a49ab02673e024812a9ee6ed8ac718a3a079d9b6417d6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca3b70411703d8c5fad3c74972887cdebac0e93c03b74a686b4f9a68000b745(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    secret_partial_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f6b493e93fa9ce7fc1db25841d8c46a5fb26eec8f7ffc750807845533581ec(
    region: builtins.str,
    encryption_key: typing.Optional[_IKey_36930160] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19cfd234d06b6e4c6e6b2a2ed284fef12f295c0e1c711aed64479eb92552af1(
    id: builtins.str,
    *,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
    hosted_rotation: typing.Optional[HostedRotation] = None,
    rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646e258e3524cdd90fdc1671a07477000e88a22fdafe11030d03223ca3834e59(
    id: builtins.str,
    *,
    target: ISecretAttachmentTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce335e18cecee4638f0f5f0a2260935204f3789b37084350d900b10d12f991fd(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4cbbb96001ec23848b7ebe26321b33cf6608bfad56b84148c8b2c5c7aa779c5(
    target: ISecretAttachmentTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813b2365bff6e358aed7f579fc6716e27eb4123fa6a5264642801eca2612359c(
    grantee: _IGrantable_4c5a91d1,
    version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8e770fc6ea8f2de45ff4c2321dd87fcdc5d9c7a51a54a8ad64e44e2e1f93f6(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abdb9320e1abb09ce5768f350a5a17c831a1e3f45fe57f111999c9b8dc0f5859(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618bb0d9f5849cf862d522a42acc9e20b275c65d9ec3a4dafef23dc7063ebec0(
    *,
    target_id: builtins.str,
    target_type: AttachmentTargetType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53c49bf7aa4c42fdf90269a1cc9647f7af714a54e8403135eb306c42f5aa8bc(
    *,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    secret_complete_arn: typing.Optional[builtins.str] = None,
    secret_partial_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24014daa44bb1f4d8d1a045f2864ba227b710f57fda38b3fe3494207dcd3f1ed(
    *,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    generate_secret_string: typing.Optional[typing.Union[SecretStringGenerator, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    replica_regions: typing.Optional[typing.Sequence[typing.Union[ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_name: typing.Optional[builtins.str] = None,
    secret_string_beta1: typing.Optional[SecretStringValueBeta1] = None,
    secret_string_value: typing.Optional[_SecretValue_c18506ef] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423d2411dce157331fb28215b3a1cef419cee98b9759b90c38af076e06727d2a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application: SecretRotationApplication,
    secret: ISecret,
    target: _IConnectable_c1c0e72c,
    vpc: _IVpc_6d1f76c4,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
    endpoint: typing.Optional[_IInterfaceVpcEndpoint_6081623d] = None,
    exclude_characters: typing.Optional[builtins.str] = None,
    master_secret: typing.Optional[ISecret] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594a14891a7de689b812116e880c1321f5841aeb7ab192b125b3d794e09fcca4(
    application_id: builtins.str,
    semantic_version: builtins.str,
    *,
    is_multi_user: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63bc4ea1dc3d2725913ea7f973ac3c35746d8be26b0db14e7e4f00146d16858(
    partition: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ae91a5d1694c69737f871316a3fe29629fef99e95451c19b8dc88ef8bcd212(
    partition: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058a3fa715cfdfddf30097b695be9ce238c8deaa53f1f6dffa8f1dc5710c9872(
    *,
    is_multi_user: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecbf9b6283a782d394b1b5ad30923f987015002920b300a30d0a5af38cf01bf(
    *,
    application: SecretRotationApplication,
    secret: ISecret,
    target: _IConnectable_c1c0e72c,
    vpc: _IVpc_6d1f76c4,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
    endpoint: typing.Optional[_IInterfaceVpcEndpoint_6081623d] = None,
    exclude_characters: typing.Optional[builtins.str] = None,
    master_secret: typing.Optional[ISecret] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae31eacb8896a374a5c4f7ba3e3e45625413cba87b97055e209cc9519f745118(
    *,
    exclude_characters: typing.Optional[builtins.str] = None,
    exclude_lowercase: typing.Optional[builtins.bool] = None,
    exclude_numbers: typing.Optional[builtins.bool] = None,
    exclude_punctuation: typing.Optional[builtins.bool] = None,
    exclude_uppercase: typing.Optional[builtins.bool] = None,
    generate_string_key: typing.Optional[builtins.str] = None,
    include_space: typing.Optional[builtins.bool] = None,
    password_length: typing.Optional[jsii.Number] = None,
    require_each_included_type: typing.Optional[builtins.bool] = None,
    secret_string_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d8e8c1bd7e931e7d9b69de30b3bc72eb4f52fa8b6344727f6ec727c99287d3(
    secret_value_from_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b8dbe810d3cec9f1b48dae765ed2ad2d7ae32399531d8640bf3b9c4daa622a(
    secret_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d3b241d255f86705eac855bdbc7082c0c0e434c10833ac31dfa08470523763(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    secret: ISecret,
    target: ISecretAttachmentTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e6ce24cf4089a0ea86dc94dcf3080b56487b9c745f8c98f453273583cbc1c3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    secret_target_attachment_secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95e4852f0780735c90d1df0cd3f363dc33c51cd8eec636292041fa94cb823ca(
    id: builtins.str,
    *,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
    hosted_rotation: typing.Optional[HostedRotation] = None,
    rotation_lambda: typing.Optional[_IFunction_6e14f09e] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93ea749b256c79a037c98ce9c2bf410c159bcb56c1fddb9e5adc0fb5479ef9a(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c9f08b1ed49815f5849cbb7a04a776b8137219a98b771bfe2626d9758ae351(
    target: ISecretAttachmentTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03199f5be15ce79d1809e9c0c666fa3b534ab5d6281c680555a279f5926d7899(
    grantee: _IGrantable_4c5a91d1,
    version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafb6c5caf6611af25f5be67ba91bb8aa23d35c64cc67da8e975cb121aa96bb5(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d00a65b80dfdb60f8730dcdc9c990e0772af83287970478dfee72d271f0bfaa(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e1a9642f84a68ab4c0d68ef8d2f5554324d0201a754ee0f383488417a70210(
    *,
    target: ISecretAttachmentTarget,
    secret: ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e225d2ecd116440be1e79d9a19262707b2eb913aca927415f45b7d0bd8ecb1(
    *,
    function_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc5360b033a9c70b6d2aaaee0b11f630f889961325760c8372a625ed3a927ed(
    *,
    function_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    master_secret: ISecret,
) -> None:
    """Type checking stubs"""
    pass
