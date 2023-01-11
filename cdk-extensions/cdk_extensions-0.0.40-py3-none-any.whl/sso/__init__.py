'''
# AWS IAM Identity Center (successor to AWS Single Sign-On)

The `@cdk-extensions/sso` package contains advanced constructs and patterns for
setting up IAM Identity Center. The constructs presented here are intended
to be replacements for equivalent AWS constructs in the CDK EC2 module, but with
additional features included.

[AWS CDK EC2 API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2-readme.html)

To import and use this module within your CDK project:

```python
import * as sso from '@cdk-extensions/sso';
```

## Objective

AWS IAM Identity Center (successor to AWS Single Sign-On) expands the capabilities of AWS Identity and Access Management (IAM) to provide a central place that brings together administration of users and their access to AWS accounts and cloud applications.

[See offical IAM Identity Center documentation](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)

### Assignment

Assigns access to a Principal for a specified AWS account using a specified permission set.  This contructs extends AWS class [Resource](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Resource.html) by adding the following properties:

| Property Name | Description |
| ------------- | ----------- |
| Instance      | The IAM Identity Center instance under which the operation will be executed |
| PermissionSet | The permission set which governs the access being assigned.  The permission set grants the principal permissions on the target |
| Principal     | The IAM Identity Center principal you wish to grant permissions to |
| Resource      | The underlying Assignment CloudFormation resource, in this case AWS::SSO::Assignment |
| Target        | The resource you wish to grant the principal entity access to using the permissions defined in the the permissionSet.  For example, an AWS account |

#### Usage

You can create an Assignment like this:

```python
// SAMPLE CODE
```

### Instance Access Control Attribute Configuration

Enables the attribute-based access control (ABAC) feature for the specified IAM Identity Center instance. You can also specify new attributes to add to your ABAC configuration during the enabling process. For more information about ABAC, see [Attribute-Based Access Control](https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html) in the IAM Identity Center User Guide. This contructs extends AWS class [Resource](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Resource.html) by adding the following properties:

| Property Name | Description |
| ------------- | ----------- |
| Attributes    | Lists the attributes that are configured for ABAC in the specified IAM Identity Center instance. This array is readonly. Changes made to the array will not be reflected in this resource. To add new attributes usethe addAttribute method |
| Instance      | The ARN of the IAM Identity Center instance under which the operation will be executed |
| Resource      | The underlying InstanceAccessControlAttributeConfiguration CloudFormation resource, in this case AWS::SSO::InstanceAccessControlAttributeConfiguration |

#### Usage

You can create an InstanceAccessControlAttributeConfiguration like this:

```python
// SAMPLE CODE
```

### Permission Set

Specifies a permission set within a specified IAM Identity Center instance. This contructs extends AWS class [Resource](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Resource.html) by adding the following properties:

| Property Name | Description |
| ------------- | ----------- |
| Description | A user friendly description providing details about the permission set |
| Instance    | The ARN of the IAM Identity Center instance under which the operation will be executed |
| Name        | The name of the permission set |
| PermissionBoundary | Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary. Specify either CustomerManagedPolicyReference to use the name and path of a customer managed policy, or ManagedPolicyArn to use the ARN of an AWS managed policy. A permissions boundary represents the maximum permissions that any policy can grant your role. For more information, see [Permissions Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) for IAM entities in the AWS Identity and Access Management User Guide. |

#### Usage

You can create an PermissionSet like this:

```python
// SAMPLE CODE
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
import aws_cdk.aws_iam
import aws_cdk.aws_sso
import constructs


class AccessControlAttribute(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.AccessControlAttribute",
):
    '''Represents and ABAC attribute in IAM Identity Center.

    These are IAM Identity Center identity store attributes that you can
    configure for use in attributes-based access control (ABAC). You can create
    permissions policies that determine who can access your AWS resources based
    upon the configured attribute values. When you enable ABAC and specify
    ``AccessControlAttributes``, IAM Identity Center passes the attribute values
    of the authenticated user into IAM for use in policy evaluation.
    '''

    def __init__(
        self,
        *,
        name: builtins.str,
        sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Creates a new instance of the AccessControlAttribute class.

        :param name: The name of the attribute associated with your identities in your identity source. This is used to map a specified attribute in your identity source with an attribute in IAM Identity Center.
        :param sources: A list of identity sources to use when mapping a specified attribute to IAM Identity Center.
        '''
        options = AccessControlAttributeOptions(name=name, sources=sources)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addSource")
    def add_source(self, source: builtins.str) -> "AccessControlAttribute":
        '''Adds an identity source to use when mapping the attribute to IAM Identity Center.

        :param source: The source to add.

        :return: The ABAC attribute the source was associated with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AccessControlAttribute.add_source)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        return typing.cast("AccessControlAttribute", jsii.invoke(self, "addSource", [source]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_sso.CfnInstanceAccessControlAttributeConfiguration.AccessControlAttributeProperty:
        '''Generates the raw CloudFormation configuration that this attribute represents within the context of a given scope.

        :param scope: The construct managing the access control attribute configuration that will consume details of this attribute.

        :return:

        The raw CloudFormation configuration that this attribute
        represents.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AccessControlAttribute.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_sso.CfnInstanceAccessControlAttributeConfiguration.AccessControlAttributeProperty, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the attribute associated with your identities in your identity source.

        This is used to map a specified attribute in your
        identity source with an attribute in IAM Identity Center.
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        '''A list of identity sources to use when mapping a specified attribute to IAM Identity Center.

        Note that the array is readonly and changes made
        to it will not be reflected when generating ABAC attribute
        configuration. To add a source to the attribute use the {@link addSource}
        method.
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))


@jsii.data_type(
    jsii_type="cdk-extensions.sso.AccessControlAttributeOptions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "sources": "sources"},
)
class AccessControlAttributeOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Configuration options for adding an ABAC attribute to IAM Identity Center.

        :param name: The name of the attribute associated with your identities in your identity source. This is used to map a specified attribute in your identity source with an attribute in IAM Identity Center.
        :param sources: A list of identity sources to use when mapping a specified attribute to IAM Identity Center.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AccessControlAttributeOptions.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the attribute associated with your identities in your identity source.

        This is used to map a specified attribute in your
        identity source with an attribute in IAM Identity Center.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of identity sources to use when mapping a specified attribute to IAM Identity Center.

        :see: `AWS::SSO::InstanceAccessControlAttributeConfiguration AccessControlAttributeValue <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattributevalue.html#cfn-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattributevalue-source>`_
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessControlAttributeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Assignment(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.Assignment",
):
    '''Assigns access to a Principal for a specified AWS account using a specified permission set.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        instance: "IInstance",
        permission_set: "IPermissionSet",
        principal: "IIdentityCenterPrincipal",
        target: "AssignmentTarget",
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Assignment class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param instance: The IAM Identity Center {@link aws-sso.IInstance | instance } under which the operation will be executed.
        :param permission_set: The permission set which governs the access being assigned. The permission set grants the {@link principal} permissions on {@link target}.
        :param principal: The IAM Identity Center principal you wish to grant permissions to.
        :param target: The resource you wish to grant the {@link principal} entity access to using the permissions defined in the {@link permissionSet}. For example, an AWS account.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Assignment.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AssignmentProps(
            instance=instance,
            permission_set=permission_set,
            principal=principal,
            target=target,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> "IInstance":
        '''The IAM Identity Center instance under which the operation will be executed.'''
        return typing.cast("IInstance", jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="permissionSet")
    def permission_set(self) -> "IPermissionSet":
        '''The permission set which governs the access being assigned.

        The
        permission set grants the {@link principal} permissions on
        {@link target}.
        '''
        return typing.cast("IPermissionSet", jsii.get(self, "permissionSet"))

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> "IIdentityCenterPrincipal":
        '''The IAM Identity Center principal you wish to grant permissions to.'''
        return typing.cast("IIdentityCenterPrincipal", jsii.get(self, "principal"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_sso.CfnAssignment:
        '''The underlying Assignment CloudFormation resource.'''
        return typing.cast(aws_cdk.aws_sso.CfnAssignment, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "AssignmentTarget":
        '''The resource you wish to grant the {@link principal} entity access to using the permissions defined in the {@link permissionSet}.

        For example,
        an AWS account.
        '''
        return typing.cast("AssignmentTarget", jsii.get(self, "target"))


@jsii.data_type(
    jsii_type="cdk-extensions.sso.AssignmentProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "instance": "instance",
        "permission_set": "permissionSet",
        "principal": "principal",
        "target": "target",
    },
)
class AssignmentProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        instance: "IInstance",
        permission_set: "IPermissionSet",
        principal: "IIdentityCenterPrincipal",
        target: "AssignmentTarget",
    ) -> None:
        '''Configuration for Assignment resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param instance: The IAM Identity Center {@link aws-sso.IInstance | instance } under which the operation will be executed.
        :param permission_set: The permission set which governs the access being assigned. The permission set grants the {@link principal} permissions on {@link target}.
        :param principal: The IAM Identity Center principal you wish to grant permissions to.
        :param target: The resource you wish to grant the {@link principal} entity access to using the permissions defined in the {@link permissionSet}. For example, an AWS account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AssignmentProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument permission_set", value=permission_set, expected_type=type_hints["permission_set"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[str, typing.Any] = {
            "instance": instance,
            "permission_set": permission_set,
            "principal": principal,
            "target": target,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region

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
    def instance(self) -> "IInstance":
        '''The IAM Identity Center {@link aws-sso.IInstance | instance } under which the operation will be executed.'''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast("IInstance", result)

    @builtins.property
    def permission_set(self) -> "IPermissionSet":
        '''The permission set which governs the access being assigned.

        The
        permission set grants the {@link principal} permissions on
        {@link target}.
        '''
        result = self._values.get("permission_set")
        assert result is not None, "Required property 'permission_set' is missing"
        return typing.cast("IPermissionSet", result)

    @builtins.property
    def principal(self) -> "IIdentityCenterPrincipal":
        '''The IAM Identity Center principal you wish to grant permissions to.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast("IIdentityCenterPrincipal", result)

    @builtins.property
    def target(self) -> "AssignmentTarget":
        '''The resource you wish to grant the {@link principal} entity access to using the permissions defined in the {@link permissionSet}.

        For example,
        an AWS account.
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("AssignmentTarget", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssignmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssignmentTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.AssignmentTarget",
):
    '''Represents a resource that can have permissions granted for using IAM Identity Center such as an AWS account.'''

    @jsii.member(jsii_name="awsAccount")
    @builtins.classmethod
    def aws_account(cls, account_id: builtins.str) -> "AssignmentTarget":
        '''Creates an assignment target that represents an AWS account.

        :param account_id: The ID of the AWS account for which permissions should be granted.

        :return: An AssignmentTarget representing the AWS account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AssignmentTarget.aws_account)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        return typing.cast("AssignmentTarget", jsii.sinvoke(cls, "awsAccount", [account_id]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        target_type: "AssignmentTargetType",
        target_id: builtins.str,
    ) -> "AssignmentTarget":
        '''An escape hatch method that allows specifying a custom target for an assignment in the event new target options are added and the provided methods for configuring targets are yet to catch up.

        It is recommended that the provided static methods be used whenever
        possible for configuring assignment targets instead of calling ``of``.

        :param target_type: The entity type for which permissions will be granted.
        :param target_id: The unique identifier specifying the entity for which permissions will be granted.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AssignmentTarget.of)
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
        return typing.cast("AssignmentTarget", jsii.sinvoke(cls, "of", [target_type, target_id]))

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        '''The unique identifier for the resource for which permissions will be granted.'''
        return typing.cast(builtins.str, jsii.get(self, "targetId"))

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> "AssignmentTargetType":
        '''The type of resource for which permissions will be granted.'''
        return typing.cast("AssignmentTargetType", jsii.get(self, "targetType"))


class AssignmentTargetType(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.AssignmentTargetType",
):
    '''Provides a wrapper around the accepted values for the IAM Identity Center `Assignment.TargetType attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-targettype>`_.

    Accepted values are provided as static properties that can be used when
    configuring an assignment.
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "AssignmentTargetType":
        '''An escape hatch method that allows specifying a custom target type in the even more options are added and the provided static types are yet to catch up.

        It is recommended that the provided static types be used when possible
        instead of calling ``of``.

        :param name: The name of the assignment target type.

        :return: An {@link AssignmentTargetType} object representing the specified type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AssignmentTargetType.of)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("AssignmentTargetType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AWS_ACCOUNT")
    def AWS_ACCOUNT(cls) -> "AssignmentTargetType":
        '''An AWS account.'''
        return typing.cast("AssignmentTargetType", jsii.sget(cls, "AWS_ACCOUNT"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name describing the type of target.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class Group(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.sso.Group"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromGroupId")
    @builtins.classmethod
    def from_group_id(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        group_id: builtins.str,
    ) -> "IGroup":
        '''
        :param scope: -
        :param id: -
        :param group_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Group.from_group_id)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast("IGroup", jsii.sinvoke(cls, "fromGroupId", [scope, id, group_id]))


@jsii.interface(jsii_type="cdk-extensions.sso.IGroup")
class IGroup(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        '''A GUID identifier for a group object in IAM Identity Center are GUIDs (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6).'''
        ...


class _IGroupProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.sso.IGroup"

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        '''A GUID identifier for a group object in IAM Identity Center are GUIDs (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6).'''
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGroup).__jsii_proxy_class__ = lambda : _IGroupProxy


@jsii.interface(jsii_type="cdk-extensions.sso.IIdentityCenterPrincipal")
class IIdentityCenterPrincipal(typing_extensions.Protocol):
    '''Represents an entity that can be granted permissions via IAM Identity Center.'''

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        '''The unique ID that identifies the entity withing IAM Identity Center.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="principalType")
    def principal_type(self) -> "IdentityCenterPrincipalType":
        '''The type of entity being represented.'''
        ...


class _IIdentityCenterPrincipalProxy:
    '''Represents an entity that can be granted permissions via IAM Identity Center.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.sso.IIdentityCenterPrincipal"

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        '''The unique ID that identifies the entity withing IAM Identity Center.'''
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="principalType")
    def principal_type(self) -> "IdentityCenterPrincipalType":
        '''The type of entity being represented.'''
        return typing.cast("IdentityCenterPrincipalType", jsii.get(self, "principalType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIdentityCenterPrincipal).__jsii_proxy_class__ = lambda : _IIdentityCenterPrincipalProxy


@jsii.interface(jsii_type="cdk-extensions.sso.IInstance")
class IInstance(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.

        For more information about ARNs, see Amazon Resource Names (ARNs) and AWS Service Namespaces in the AWS General Reference.

        :see: `AWS::SSO::Assignment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-instancearn>`_
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The ID of the IAM Identity Center instance under which the operation will be executed.'''
        ...


class _IInstanceProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.sso.IInstance"

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.

        For more information about ARNs, see Amazon Resource Names (ARNs) and AWS Service Namespaces in the AWS General Reference.

        :see: `AWS::SSO::Assignment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-instancearn>`_
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The ID of the IAM Identity Center instance under which the operation will be executed.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInstance).__jsii_proxy_class__ = lambda : _IInstanceProxy


@jsii.interface(jsii_type="cdk-extensions.sso.IPermissionSet")
class IPermissionSet(typing_extensions.Protocol):
    '''Represents an IAM Identity Center permission set resource.'''

    @builtins.property
    @jsii.member(jsii_name="permissionSetArn")
    def permission_set_arn(self) -> builtins.str:
        ...


class _IPermissionSetProxy:
    '''Represents an IAM Identity Center permission set resource.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.sso.IPermissionSet"

    @builtins.property
    @jsii.member(jsii_name="permissionSetArn")
    def permission_set_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissionSetArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPermissionSet).__jsii_proxy_class__ = lambda : _IPermissionSetProxy


@jsii.interface(jsii_type="cdk-extensions.sso.IUser")
class IUser(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        '''A GUID identifier for a user object in IAM Identity Center (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6).'''
        ...


class _IUserProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.sso.IUser"

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        '''A GUID identifier for a user object in IAM Identity Center (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6).'''
        return typing.cast(builtins.str, jsii.get(self, "userId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUser).__jsii_proxy_class__ = lambda : _IUserProxy


class IdentityCenterPrincipalType(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.IdentityCenterPrincipalType",
):
    '''Provides a wrapper around the accepted values for the IAM Identity Center `Assignment.PrincipalType attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-principaltype>`_.

    Accepted values are provided as static properties that can be used when
    configuring an assignment.
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "IdentityCenterPrincipalType":
        '''An escape hatch method that allows specifying a custom principal types in the even more options are added and the provided static types are yet to catch up.

        It is recommended that the provided static types be used when possible
        instead of calling ``of``.

        :param name: The name for a type of IAM Identity Center Principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IdentityCenterPrincipalType.of)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("IdentityCenterPrincipalType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GROUP")
    def GROUP(cls) -> "IdentityCenterPrincipalType":
        '''An IAM Identity Center group.'''
        return typing.cast("IdentityCenterPrincipalType", jsii.sget(cls, "GROUP"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="USER")
    def USER(cls) -> "IdentityCenterPrincipalType":
        '''An IAM Identity Center user.'''
        return typing.cast("IdentityCenterPrincipalType", jsii.sget(cls, "USER"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name for a type of IAM Identity Center Principal.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class Instance(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.sso.Instance"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        arn: builtins.str,
    ) -> IInstance:
        '''
        :param scope: -
        :param id: -
        :param arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Instance.from_arn)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast(IInstance, jsii.sinvoke(cls, "fromArn", [scope, id, arn]))

    @jsii.member(jsii_name="fromInstanceId")
    @builtins.classmethod
    def from_instance_id(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        instance_id: builtins.str,
    ) -> IInstance:
        '''
        :param scope: -
        :param id: -
        :param instance_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Instance.from_instance_id)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
        return typing.cast(IInstance, jsii.sinvoke(cls, "fromInstanceId", [scope, id, instance_id]))


class InstanceAccessControlAttributeConfiguration(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.InstanceAccessControlAttributeConfiguration",
):
    '''Enables the attribute-based access control (ABAC) feature for the specified IAM Identity Center instance.

    You can also specify new attributes to add to
    your ABAC configuration during the enabling process. For more information
    about ABAC, see `Attribute-Based Access Control <https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html>`_ in the IAM Identity Center
    User Guide.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        instance: IInstance,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the InstanceAccessControlAttributeConfiguration class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param instance: The ARN of the IAM Identity Center instance under which the operation will be executed.
        :param attribute_mapping: Lists the attributes that are configured for ABAC in the specified IAM Identity Center instance.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(InstanceAccessControlAttributeConfiguration.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InstanceAccessControlAttributeConfigurationProps(
            instance=instance,
            attribute_mapping=attribute_mapping,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAttribute")
    def add_attribute(
        self,
        key: builtins.str,
        *sources: builtins.str,
    ) -> AccessControlAttribute:
        '''Adds a new ABAC attribute in the specified IAM Identity Center instance.

        :param key: The name of the attribute associated with your identities in your identity source. This is used to map a specified attribute in your identity source with an attribute in IAM Identity Center.
        :param sources: The identity sources to use when mapping a specified attribute to IAM Identity Center.

        :return:

        An AccessControlAttribute resource that will be applied to the
        configuration and supports continued management.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(InstanceAccessControlAttributeConfiguration.add_attribute)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument sources", value=sources, expected_type=typing.Tuple[type_hints["sources"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(AccessControlAttribute, jsii.invoke(self, "addAttribute", [key, *sources]))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.List[AccessControlAttribute]:
        '''Lists the attributes that are configured for ABAC in the specified IAM Identity Center instance.

        This array is readonly. Changes made to the
        array will not be reflected in this resource. To add new attributes use
        the ``{@link addAttribute}`` method.
        '''
        return typing.cast(typing.List[AccessControlAttribute], jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> IInstance:
        '''The ARN of the IAM Identity Center {@link aws-sso.IInstance | instance } under which the operation will be executed.'''
        return typing.cast(IInstance, jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(
        self,
    ) -> aws_cdk.aws_sso.CfnInstanceAccessControlAttributeConfiguration:
        '''The underlying InstanceAccessControlAttributeConfiguration CloudFormation resource.'''
        return typing.cast(aws_cdk.aws_sso.CfnInstanceAccessControlAttributeConfiguration, jsii.get(self, "resource"))


@jsii.data_type(
    jsii_type="cdk-extensions.sso.InstanceAccessControlAttributeConfigurationProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "instance": "instance",
        "attribute_mapping": "attributeMapping",
    },
)
class InstanceAccessControlAttributeConfigurationProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        instance: IInstance,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''Configuration for InstanceAccessControlAttributeConfiguration resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param instance: The ARN of the IAM Identity Center instance under which the operation will be executed.
        :param attribute_mapping: Lists the attributes that are configured for ABAC in the specified IAM Identity Center instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(InstanceAccessControlAttributeConfigurationProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument attribute_mapping", value=attribute_mapping, expected_type=type_hints["attribute_mapping"])
        self._values: typing.Dict[str, typing.Any] = {
            "instance": instance,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping

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
    def instance(self) -> IInstance:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.'''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(IInstance, result)

    @builtins.property
    def attribute_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''Lists the attributes that are configured for ABAC in the specified IAM Identity Center instance.'''
        result = self._values.get("attribute_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceAccessControlAttributeConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInstance)
class InstanceBase(
    aws_cdk.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.sso.InstanceBase",
):
    def __init__(
        self,
        scope: constructs.Construct,
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
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(InstanceBase.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    @abc.abstractmethod
    def instance_arn(self) -> builtins.str:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.

        For more information about ARNs, see Amazon Resource Names (ARNs) and AWS Service Namespaces in the AWS General Reference.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    @abc.abstractmethod
    def instance_id(self) -> builtins.str:
        '''The ID of the IAM Identity Center instance under which the operation will be executed.'''
        ...


class _InstanceBaseProxy(
    InstanceBase,
    jsii.proxy_for(aws_cdk.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.

        For more information about ARNs, see Amazon Resource Names (ARNs) and AWS Service Namespaces in the AWS General Reference.
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The ID of the IAM Identity Center instance under which the operation will be executed.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, InstanceBase).__jsii_proxy_class__ = lambda : _InstanceBaseProxy


@jsii.implements(IPermissionSet)
class PermissionSet(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.PermissionSet",
):
    '''Specifies a permission set within a specified IAM Identity Center instance.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        instance: IInstance,
        description: typing.Optional[builtins.str] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional["PermissionsBoundary"] = None,
        relay_state: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[aws_cdk.Duration] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the PermissionSet class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param instance: The ARN of the IAM Identity Center instance under which the operation will be executed.
        :param description: A user friendly description providing details about the permission set.
        :param inline_policies: Adds inline policy documents that will be embedded in the permission set.
        :param managed_policies: A list of the IAM managed policies that you want to attach to the permission set. Managed policies specified here must be AWS managed. To reference custom managed policies use the {@link PermissionSet.addCustomerManagedPolicy} method.
        :param name: The name of the permission set.
        :param permissions_boundary: Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary. Specify either CustomerManagedPolicyReference to use the name and path of a customer managed policy, or ManagedPolicyArn to use the ARN of an AWS managed policy. A permissions boundary represents the maximum permissions that any policy can grant your role. For more information, see `Permissions boundaries <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ for IAM entities in the AWS Identity and Access Management User Guide.
        :param relay_state: Used to redirect users within the application during the federation authentication process. For example, you can redirect users to a specific page that is most applicable to their job after singing in to an AWS account.
        :param session_duration: The length of time that the application user sessions are valid for.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PermissionSet.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PermissionSetProps(
            instance=instance,
            description=description,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            name=name,
            permissions_boundary=permissions_boundary,
            relay_state=relay_state,
            session_duration=session_duration,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        arn: builtins.str,
    ) -> IPermissionSet:
        '''
        :param scope: -
        :param id: -
        :param arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PermissionSet.from_arn)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast(IPermissionSet, jsii.sinvoke(cls, "fromArn", [scope, id, arn]))

    @jsii.member(jsii_name="addCustomerManagedPolicy")
    def add_customer_managed_policy(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> "ReferencedManagedPolicy":
        '''Adds a custom managed policy to the permission set.

        When using customer
        managed policies it is required that a managed policy with a matching
        name and path exist in any AWS account for which the permission set
        will be assigned.

        :param name: The name of the customer managed policy.
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User Guide. This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (``\\u0021``) through the DEL character (``\\u007F``), including most punctuation characters, digits, and upper and lowercased letters. Default: '/''

        :return:

        A dynamically generated ManagedPolicy class that can be used
        to create compatible managed policies in other accounts.
        '''
        options = ReferenceOptions(name=name, path=path)

        return typing.cast("ReferencedManagedPolicy", jsii.invoke(self, "addCustomerManagedPolicy", [options]))

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(
        self,
        policy: aws_cdk.aws_iam.IManagedPolicy,
    ) -> "PermissionSet":
        '''Adds a new Managed Policy to the permission set.

        Only Managed Policies
        created and maintained by AWS are supported. To add a custom Managed
        Policy that you control use the {@link addCustomerManagedPolicy} method.

        :param policy: The AWS Managed Policy to associate with the Permission Set.

        :return: The Permission Set resource the Managed Policy was added to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PermissionSet.add_managed_policy)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast("PermissionSet", jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToPrincipalPolicyResult:
        '''Adds a permission to the permission set's default policy document.

        If there is no default policy attached to this permission set, it will be created.

        :param statement: The permission statement to add to the policy document.

        :return:

        An `AddToPrincipalPolicyResult <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_iam.AddToPrincipalPolicyResult.html>`_ object that provides details of
        the result of the operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PermissionSet.add_to_principal_policy)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(aws_cdk.aws_iam.AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> IInstance:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.'''
        return typing.cast(IInstance, jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="permissionSetArn")
    def permission_set_arn(self) -> builtins.str:
        '''The permission set ARN of the permission set, such as ``arn:aws:sso:::permissionSet/ins-instanceid/ps-permissionsetid``.'''
        return typing.cast(builtins.str, jsii.get(self, "permissionSetArn"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_sso.CfnPermissionSet:
        '''The underlying PermissionSet CloudFormation resource.'''
        return typing.cast(aws_cdk.aws_sso.CfnPermissionSet, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A user friendly description providing details about the permission set.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the permission set.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional["PermissionsBoundary"]:
        '''Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary.

        Specify either
        CustomerManagedPolicyReference to use the name and path of a customer
        managed policy, or ManagedPolicyArn to use the ARN of an AWS managed
        policy. A permissions boundary represents the maximum permissions that
        any policy can grant your role. For more information, see `Permissions
        boundaries <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ for IAM entities in the AWS Identity and Access Management
        User Guide.
        '''
        return typing.cast(typing.Optional["PermissionsBoundary"], jsii.get(self, "permissionsBoundary"))

    @builtins.property
    @jsii.member(jsii_name="relayState")
    def relay_state(self) -> typing.Optional[builtins.str]:
        '''Used to redirect users within the application during the federation authentication process.

        For example, you can redirect users to a
        specific page that is most applicable to their job after singing in to
        an AWS account.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relayState"))

    @builtins.property
    @jsii.member(jsii_name="sessionDuration")
    def session_duration(self) -> typing.Optional[aws_cdk.Duration]:
        '''The length of time that the application user sessions are valid for.'''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "sessionDuration"))


@jsii.data_type(
    jsii_type="cdk-extensions.sso.PermissionSetProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "instance": "instance",
        "description": "description",
        "inline_policies": "inlinePolicies",
        "managed_policies": "managedPolicies",
        "name": "name",
        "permissions_boundary": "permissionsBoundary",
        "relay_state": "relayState",
        "session_duration": "sessionDuration",
    },
)
class PermissionSetProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        instance: IInstance,
        description: typing.Optional[builtins.str] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional["PermissionsBoundary"] = None,
        relay_state: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''Configuration for PermissionSet resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param instance: The ARN of the IAM Identity Center instance under which the operation will be executed.
        :param description: A user friendly description providing details about the permission set.
        :param inline_policies: Adds inline policy documents that will be embedded in the permission set.
        :param managed_policies: A list of the IAM managed policies that you want to attach to the permission set. Managed policies specified here must be AWS managed. To reference custom managed policies use the {@link PermissionSet.addCustomerManagedPolicy} method.
        :param name: The name of the permission set.
        :param permissions_boundary: Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary. Specify either CustomerManagedPolicyReference to use the name and path of a customer managed policy, or ManagedPolicyArn to use the ARN of an AWS managed policy. A permissions boundary represents the maximum permissions that any policy can grant your role. For more information, see `Permissions boundaries <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ for IAM entities in the AWS Identity and Access Management User Guide.
        :param relay_state: Used to redirect users within the application during the federation authentication process. For example, you can redirect users to a specific page that is most applicable to their job after singing in to an AWS account.
        :param session_duration: The length of time that the application user sessions are valid for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PermissionSetProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument inline_policies", value=inline_policies, expected_type=type_hints["inline_policies"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument relay_state", value=relay_state, expected_type=type_hints["relay_state"])
            check_type(argname="argument session_duration", value=session_duration, expected_type=type_hints["session_duration"])
        self._values: typing.Dict[str, typing.Any] = {
            "instance": instance,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if description is not None:
            self._values["description"] = description
        if inline_policies is not None:
            self._values["inline_policies"] = inline_policies
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if name is not None:
            self._values["name"] = name
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if relay_state is not None:
            self._values["relay_state"] = relay_state
        if session_duration is not None:
            self._values["session_duration"] = session_duration

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
    def instance(self) -> IInstance:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.'''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(IInstance, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user friendly description providing details about the permission set.

        :see: `AWS::SSO::PermissionSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-description>`_
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_policies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]]:
        '''Adds inline policy documents that will be embedded in the permission set.

        :see: `AWS::SSO::PermissionSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-inlinepolicy>`_
        '''
        result = self._values.get("inline_policies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]], result)

    @builtins.property
    def managed_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.IManagedPolicy]]:
        '''A list of the IAM managed policies that you want to attach to the permission set.

        Managed policies specified here must be AWS managed.
        To reference custom managed policies use the {@link PermissionSet.addCustomerManagedPolicy}
        method.

        :see: `AWS::SSO::PermissionSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-managedpolicies>`_
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IManagedPolicy]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the permission set.

        :see: `AWS::SSO::PermissionSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-name>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional["PermissionsBoundary"]:
        '''Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary.

        Specify either
        CustomerManagedPolicyReference to use the name and path of a customer
        managed policy, or ManagedPolicyArn to use the ARN of an AWS managed
        policy. A permissions boundary represents the maximum permissions that
        any policy can grant your role. For more information, see `Permissions
        boundaries <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ for IAM entities in the AWS Identity and Access Management
        User Guide.

        :see: `AWS::SSO::PermissionSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-permissionsboundary>`_
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional["PermissionsBoundary"], result)

    @builtins.property
    def relay_state(self) -> typing.Optional[builtins.str]:
        '''Used to redirect users within the application during the federation authentication process.

        For example, you can redirect users to a
        specific page that is most applicable to their job after singing in to
        an AWS account.

        :see: `AWS::SSO::PermissionSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-relaystatetype>`_
        '''
        result = self._values.get("relay_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_duration(self) -> typing.Optional[aws_cdk.Duration]:
        '''The length of time that the application user sessions are valid for.

        :see: `AWS::SSO::PermissionSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-sessionduration>`_
        '''
        result = self._values.get("session_duration")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PermissionSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PermissionsBoundary(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.sso.PermissionsBoundary",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromManagedPolicy")
    @builtins.classmethod
    def from_managed_policy(
        cls,
        policy: aws_cdk.aws_iam.IManagedPolicy,
    ) -> "ManagedPolicyPermissionsBoundary":
        '''
        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PermissionsBoundary.from_managed_policy)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast("ManagedPolicyPermissionsBoundary", jsii.sinvoke(cls, "fromManagedPolicy", [policy]))

    @jsii.member(jsii_name="fromReference")
    @builtins.classmethod
    def from_reference(
        cls,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> "ReferencedPermissionsBoundary":
        '''
        :param name: The name of the customer managed policy.
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User Guide. This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (``\\u0021``) through the DEL character (``\\u007F``), including most punctuation characters, digits, and upper and lowercased letters. Default: '/''
        '''
        options = ReferenceOptions(name=name, path=path)

        return typing.cast("ReferencedPermissionsBoundary", jsii.sinvoke(cls, "fromReference", [options]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_sso.CfnPermissionSet.PermissionsBoundaryProperty:
        '''
        :param scope: -
        '''
        ...


class _PermissionsBoundaryProxy(PermissionsBoundary):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_sso.CfnPermissionSet.PermissionsBoundaryProperty:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PermissionsBoundary.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_sso.CfnPermissionSet.PermissionsBoundaryProperty, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PermissionsBoundary).__jsii_proxy_class__ = lambda : _PermissionsBoundaryProxy


@jsii.data_type(
    jsii_type="cdk-extensions.sso.ReferenceOptions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class ReferenceOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for creating a referenced customer managed policy.

        :param name: The name of the customer managed policy.
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User Guide. This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (``\\u0021``) through the DEL character (``\\u007F``), including most punctuation characters, digits, and upper and lowercased letters. Default: '/''
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ReferenceOptions.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the customer managed policy.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User
        Guide.

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows a string of characters consisting of either a
        forward slash (/) by itself or a string that must begin and end with
        forward slashes. In addition, it can contain any ASCII character from
        the ! (``\\u0021``) through the DEL character (``\\u007F``), including most
        punctuation characters, digits, and upper and lowercased letters.

        :default: '/''
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReferencedManagedPolicy(
    aws_cdk.aws_iam.ManagedPolicy,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.sso.ReferencedManagedPolicy",
):
    '''A managed policy that is referenced via IAM Identity Center.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        document: typing.Optional[aws_cdk.aws_iam.PolicyDocument] = None,
        groups: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IGroup]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        statements: typing.Optional[typing.Sequence[aws_cdk.aws_iam.PolicyStatement]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''Creates a new instance of the ReferencedManagedPolicy class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param description: A friendly description of the policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed.
        :param document: The policy document that you want to use as the content for the new policy.
        :param groups: The groups to attach the policy to. When creating managed policies that will be referenced by IAM identity center it is possible to associate them with other resources such as users, groups, and roles. However, this is typically not done as IAM Identity Center will handle configuring associations in the background.
        :param roles: The roles to attach the policy to. When creating managed policies that will be referenced by IAM identity center it is possible to associate them with other resources such as users, groups, and roles. However, this is typically not done as IAM Identity Center will handle configuring associations in the background.
        :param statements: Initial set of permissions to add to this policy document.
        :param users: The users to attach the policy to. When creating managed policies that will be referenced by IAM identity center it is possible to associate them with other resources such as users, groups, and roles. However, this is typically not done as IAM Identity Center will handle configuring associations in the background.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ReferencedManagedPolicy.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ReferencedManagedPolicyProps(
            description=description,
            document=document,
            groups=groups,
            roles=roles,
            statements=statements,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> "ReferencedManagedPolicy":
        '''Dynamically generates a new class that can be used to create a managed policy that matches a reference in IAM Identity Center.

        :param name: The name of the customer managed policy.
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User Guide. This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (``\\u0021``) through the DEL character (``\\u007F``), including most punctuation characters, digits, and upper and lowercased letters. Default: '/''

        :return:

        A dynamically generated class that will match the provided
        reference configuration.
        '''
        options = ReferenceOptions(name=name, path=path)

        return typing.cast("ReferencedManagedPolicy", jsii.sinvoke(cls, "of", [options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="policyName")
    def POLICY_NAME(cls) -> builtins.str:
        '''The name of the managed policy.'''
        return typing.cast(builtins.str, jsii.sget(cls, "policyName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="policyPath")
    def POLICY_PATH(cls) -> typing.Optional[builtins.str]:
        '''The path for the managed policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User
        Guide.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "policyPath"))

    @builtins.property
    @jsii.member(jsii_name="referencedName")
    @abc.abstractmethod
    def referenced_name(self) -> builtins.str:
        '''The name of the managed policy.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="referencedPath")
    @abc.abstractmethod
    def referenced_path(self) -> typing.Optional[builtins.str]:
        '''The path for the managed policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User
        Guide.
        '''
        ...


class _ReferencedManagedPolicyProxy(ReferencedManagedPolicy):
    @builtins.property
    @jsii.member(jsii_name="referencedName")
    def referenced_name(self) -> builtins.str:
        '''The name of the managed policy.'''
        return typing.cast(builtins.str, jsii.get(self, "referencedName"))

    @builtins.property
    @jsii.member(jsii_name="referencedPath")
    def referenced_path(self) -> typing.Optional[builtins.str]:
        '''The path for the managed policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User
        Guide.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referencedPath"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ReferencedManagedPolicy).__jsii_proxy_class__ = lambda : _ReferencedManagedPolicyProxy


@jsii.data_type(
    jsii_type="cdk-extensions.sso.ReferencedManagedPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "document": "document",
        "groups": "groups",
        "roles": "roles",
        "statements": "statements",
        "users": "users",
    },
)
class ReferencedManagedPolicyProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        document: typing.Optional[aws_cdk.aws_iam.PolicyDocument] = None,
        groups: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IGroup]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        statements: typing.Optional[typing.Sequence[aws_cdk.aws_iam.PolicyStatement]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''Represents configuration options when creating a managed policy from a class generated when adding a custom policy reference.

        :param description: A friendly description of the policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed.
        :param document: The policy document that you want to use as the content for the new policy.
        :param groups: The groups to attach the policy to. When creating managed policies that will be referenced by IAM identity center it is possible to associate them with other resources such as users, groups, and roles. However, this is typically not done as IAM Identity Center will handle configuring associations in the background.
        :param roles: The roles to attach the policy to. When creating managed policies that will be referenced by IAM identity center it is possible to associate them with other resources such as users, groups, and roles. However, this is typically not done as IAM Identity Center will handle configuring associations in the background.
        :param statements: Initial set of permissions to add to this policy document.
        :param users: The users to attach the policy to. When creating managed policies that will be referenced by IAM identity center it is possible to associate them with other resources such as users, groups, and roles. However, this is typically not done as IAM Identity Center will handle configuring associations in the background.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ReferencedManagedPolicyProps.__init__)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if document is not None:
            self._values["document"] = document
        if groups is not None:
            self._values["groups"] = groups
        if roles is not None:
            self._values["roles"] = roles
        if statements is not None:
            self._values["statements"] = statements
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A friendly description of the policy.

        Typically used to store information about the permissions defined in the
        policy. For example, "Grants access to production DynamoDB tables."

        The policy description is immutable. After a value is assigned, it
        cannot be changed.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        '''The policy document that you want to use as the content for the new policy.'''
        result = self._values.get("document")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.PolicyDocument], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.IGroup]]:
        '''The groups to attach the policy to.

        When creating managed policies that will be referenced by IAM identity
        center it is possible to associate them with other resources such as
        users, groups, and roles. However, this is typically not done as IAM
        Identity Center will handle configuring associations in the background.
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IGroup]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.IRole]]:
        '''The roles to attach the policy to.

        When creating managed policies that will be referenced by IAM identity
        center it is possible to associate them with other resources such as
        users, groups, and roles. However, this is typically not done as IAM
        Identity Center will handle configuring associations in the background.
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IRole]], result)

    @builtins.property
    def statements(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        '''Initial set of permissions to add to this policy document.'''
        result = self._values.get("statements")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.IUser]]:
        '''The users to attach the policy to.

        When creating managed policies that will be referenced by IAM identity
        center it is possible to associate them with other resources such as
        users, groups, and roles. However, this is typically not done as IAM
        Identity Center will handle configuring associations in the background.
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IUser]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferencedManagedPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReferencedPermissionsBoundary(
    PermissionsBoundary,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.ReferencedPermissionsBoundary",
):
    def __init__(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the customer managed policy.
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the IAM User Guide. This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (``\\u0021``) through the DEL character (``\\u007F``), including most punctuation characters, digits, and upper and lowercased letters. Default: '/''
        '''
        options = ReferenceOptions(name=name, path=path)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.IConstruct,
    ) -> aws_cdk.aws_sso.CfnPermissionSet.PermissionsBoundaryProperty:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ReferencedPermissionsBoundary.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(aws_cdk.aws_sso.CfnPermissionSet.PermissionsBoundaryProperty, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="referencedPolicy")
    def referenced_policy(self) -> ReferencedManagedPolicy:
        return typing.cast(ReferencedManagedPolicy, jsii.get(self, "referencedPolicy"))


class User(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.sso.User"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromUserId")
    @builtins.classmethod
    def from_user_id(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        user_id: builtins.str,
    ) -> IUser:
        '''
        :param scope: -
        :param id: -
        :param user_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(User.from_user_id)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        return typing.cast(IUser, jsii.sinvoke(cls, "fromUserId", [scope, id, user_id]))


@jsii.implements(IUser, IIdentityCenterPrincipal)
class UserBase(
    aws_cdk.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.sso.UserBase",
):
    def __init__(
        self,
        scope: constructs.IConstruct,
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
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(UserBase.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="principalId")
    @abc.abstractmethod
    def principal_id(self) -> builtins.str:
        '''The unique ID that identifies the entity withing IAM Identity Center.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="principalType")
    def principal_type(self) -> IdentityCenterPrincipalType:
        '''The type of entity being represented.'''
        return typing.cast(IdentityCenterPrincipalType, jsii.get(self, "principalType"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    @abc.abstractmethod
    def user_id(self) -> builtins.str:
        '''A GUID identifier for a user object in IAM Identity Center (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6).'''
        ...


class _UserBaseProxy(
    UserBase,
    jsii.proxy_for(aws_cdk.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        '''The unique ID that identifies the entity withing IAM Identity Center.'''
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        '''A GUID identifier for a user object in IAM Identity Center (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6).'''
        return typing.cast(builtins.str, jsii.get(self, "userId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, UserBase).__jsii_proxy_class__ = lambda : _UserBaseProxy


@jsii.implements(IGroup, IIdentityCenterPrincipal)
class GroupBase(
    aws_cdk.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.sso.GroupBase",
):
    def __init__(
        self,
        scope: constructs.IConstruct,
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
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GroupBase.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="groupId")
    @abc.abstractmethod
    def group_id(self) -> builtins.str:
        '''A GUID identifier for a group object in IAM Identity Center are GUIDs (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="principalId")
    @abc.abstractmethod
    def principal_id(self) -> builtins.str:
        '''The unique ID that identifies the entity withing IAM Identity Center.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="principalType")
    def principal_type(self) -> IdentityCenterPrincipalType:
        '''The type of entity being represented.'''
        return typing.cast(IdentityCenterPrincipalType, jsii.get(self, "principalType"))


class _GroupBaseProxy(
    GroupBase,
    jsii.proxy_for(aws_cdk.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        '''A GUID identifier for a group object in IAM Identity Center are GUIDs (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6).'''
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        '''The unique ID that identifies the entity withing IAM Identity Center.'''
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, GroupBase).__jsii_proxy_class__ = lambda : _GroupBaseProxy


class ManagedPolicyPermissionsBoundary(
    PermissionsBoundary,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.sso.ManagedPolicyPermissionsBoundary",
):
    def __init__(self, policy: aws_cdk.aws_iam.IManagedPolicy) -> None:
        '''
        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ManagedPolicyPermissionsBoundary.__init__)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        jsii.create(self.__class__, self, [policy])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.IConstruct,
    ) -> aws_cdk.aws_sso.CfnPermissionSet.PermissionsBoundaryProperty:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ManagedPolicyPermissionsBoundary.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(aws_cdk.aws_sso.CfnPermissionSet.PermissionsBoundaryProperty, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="managedPolicy")
    def managed_policy(self) -> aws_cdk.aws_iam.IManagedPolicy:
        return typing.cast(aws_cdk.aws_iam.IManagedPolicy, jsii.get(self, "managedPolicy"))


__all__ = [
    "AccessControlAttribute",
    "AccessControlAttributeOptions",
    "Assignment",
    "AssignmentProps",
    "AssignmentTarget",
    "AssignmentTargetType",
    "Group",
    "GroupBase",
    "IGroup",
    "IIdentityCenterPrincipal",
    "IInstance",
    "IPermissionSet",
    "IUser",
    "IdentityCenterPrincipalType",
    "Instance",
    "InstanceAccessControlAttributeConfiguration",
    "InstanceAccessControlAttributeConfigurationProps",
    "InstanceBase",
    "ManagedPolicyPermissionsBoundary",
    "PermissionSet",
    "PermissionSetProps",
    "PermissionsBoundary",
    "ReferenceOptions",
    "ReferencedManagedPolicy",
    "ReferencedManagedPolicyProps",
    "ReferencedPermissionsBoundary",
    "User",
    "UserBase",
]

publication.publish()
