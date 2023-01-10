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
import aws_cdk.aws_codebuild
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_ram
import constructs


@jsii.interface(jsii_type="cdk-extensions.ram.ISharedPrincipal")
class ISharedPrincipal(typing_extensions.Protocol):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> builtins.str:
        '''
        :param scope: -
        '''
        ...


class _ISharedPrincipalProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ram.ISharedPrincipal"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ISharedPrincipal.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISharedPrincipal).__jsii_proxy_class__ = lambda : _ISharedPrincipalProxy


@jsii.interface(jsii_type="cdk-extensions.ram.ISharedResource")
class ISharedResource(typing_extensions.Protocol):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> builtins.str:
        '''
        :param scope: -
        '''
        ...


class _ISharedResourceProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ram.ISharedResource"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ISharedResource.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISharedResource).__jsii_proxy_class__ = lambda : _ISharedResourceProxy


class ResourceShare(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ram.ResourceShare",
):
    '''Creates a resource share that can used to share AWS resources with other AWS accounts, organizations, or organizational units (OU's).

    :see: `AWS::RAM::ResourceShare <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        allow_external_principals: typing.Optional[builtins.bool] = None,
        auto_discover_accounts: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[ISharedPrincipal]] = None,
        resources: typing.Optional[typing.Sequence[ISharedResource]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the ResourceShare class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param allow_external_principals: Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share. A value of ``true`` lets you share with individual AWS accounts that are not in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. Default: true
        :param auto_discover_accounts: Controls whether the resource share should attempt to search for AWS accounts that are part of the same CDK application. Any accounts is finds will be added to the resource automatically and will be able to use the shared resources.
        :param name: Specifies the name of the resource share.
        :param principals: Specifies a list of one or more principals to associate with the resource share.
        :param resources: Specifies a list of AWS resources to share with the configured principal accounts and organizations.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ResourceShare.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ResourceShareProps(
            allow_external_principals=allow_external_principals,
            auto_discover_accounts=auto_discover_accounts,
            name=name,
            principals=principals,
            resources=resources,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addPrincipal")
    def add_principal(self, principal: ISharedPrincipal) -> None:
        '''
        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ResourceShare.add_principal)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(None, jsii.invoke(self, "addPrincipal", [principal]))

    @jsii.member(jsii_name="addResource")
    def add_resource(self, resource: ISharedResource) -> None:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ResourceShare.add_resource)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(None, jsii.invoke(self, "addResource", [resource]))

    @jsii.member(jsii_name="enableAutoDiscovery")
    def enable_auto_discovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "enableAutoDiscovery", []))

    @builtins.property
    @jsii.member(jsii_name="autoDiscovery")
    def auto_discovery(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "autoDiscovery"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Specifies the name of the resource share.

        :see: `ResourceShare.Name <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name>`_
        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_ram.CfnResourceShare:
        '''The underlying ResourceShare CloudFormation resource.

        :see: `AWS::RAM::ResourceShare <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html>`_
        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_ram.CfnResourceShare, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="allowExternalPrincipals")
    def allow_external_principals(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share.

        A value of ``true``
        lets you share with individual AWS accounts that are not in your
        organization. A value of ``false`` only has meaning if your account is a
        member of an AWS Organization.

        In order for an account to be auto discovered it must be part of the same
        CDK application. It must also be an explicitly defined environment and not
        environment agnostic.

        :see: `CDK Environments <https://docs.aws.amazon.com/cdk/v2/guide/environments.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allowExternalPrincipals"))


@jsii.data_type(
    jsii_type="cdk-extensions.ram.ResourceShareProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "allow_external_principals": "allowExternalPrincipals",
        "auto_discover_accounts": "autoDiscoverAccounts",
        "name": "name",
        "principals": "principals",
        "resources": "resources",
    },
)
class ResourceShareProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        allow_external_principals: typing.Optional[builtins.bool] = None,
        auto_discover_accounts: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[ISharedPrincipal]] = None,
        resources: typing.Optional[typing.Sequence[ISharedResource]] = None,
    ) -> None:
        '''Configuration for ResourceShare resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param allow_external_principals: Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share. A value of ``true`` lets you share with individual AWS accounts that are not in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. Default: true
        :param auto_discover_accounts: Controls whether the resource share should attempt to search for AWS accounts that are part of the same CDK application. Any accounts is finds will be added to the resource automatically and will be able to use the shared resources.
        :param name: Specifies the name of the resource share.
        :param principals: Specifies a list of one or more principals to associate with the resource share.
        :param resources: Specifies a list of AWS resources to share with the configured principal accounts and organizations.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ResourceShareProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument auto_discover_accounts", value=auto_discover_accounts, expected_type=type_hints["auto_discover_accounts"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if auto_discover_accounts is not None:
            self._values["auto_discover_accounts"] = auto_discover_accounts
        if name is not None:
            self._values["name"] = name
        if principals is not None:
            self._values["principals"] = principals
        if resources is not None:
            self._values["resources"] = resources

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
    def allow_external_principals(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share.

        A value of ``true``
        lets you share with individual AWS accounts that are not in your
        organization. A value of ``false`` only has meaning if your account is a
        member of an AWS Organization.

        :default: true

        :see: `ResourceShare.AllowExternalPrinicpals <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals>`_
        '''
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_discover_accounts(self) -> typing.Optional[builtins.bool]:
        '''Controls whether the resource share should attempt to search for AWS accounts that are part of the same CDK application.

        Any accounts is finds
        will be added to the resource automatically and will be able to use the
        shared resources.
        '''
        result = self._values.get("auto_discover_accounts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the resource share.

        :see: `ResourceShare.Name <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[ISharedPrincipal]]:
        '''Specifies a list of one or more principals to associate with the resource share.

        :see: `ResourceShare.Prinicipals <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals>`_
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[ISharedPrincipal]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[ISharedResource]]:
        '''Specifies a list of AWS resources to share with the configured principal accounts and organizations.

        :see: `ResourceShare.ResourceArns <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns>`_
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[ISharedResource]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISharedPrincipal)
class SharedPrincipal(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ram.SharedPrincipal",
):
    @jsii.member(jsii_name="fromAccountId")
    @builtins.classmethod
    def from_account_id(cls, account: builtins.str) -> "SharedPrincipal":
        '''
        :param account: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedPrincipal.from_account_id)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
        return typing.cast("SharedPrincipal", jsii.sinvoke(cls, "fromAccountId", [account]))

    @jsii.member(jsii_name="fromConstruct")
    @builtins.classmethod
    def from_construct(cls, construct: constructs.IConstruct) -> "SharedPrincipal":
        '''
        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedPrincipal.from_construct)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast("SharedPrincipal", jsii.sinvoke(cls, "fromConstruct", [construct]))

    @jsii.member(jsii_name="fromOrganizationalUnitArn")
    @builtins.classmethod
    def from_organizational_unit_arn(cls, arn: builtins.str) -> "SharedPrincipal":
        '''
        :param arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedPrincipal.from_organizational_unit_arn)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast("SharedPrincipal", jsii.sinvoke(cls, "fromOrganizationalUnitArn", [arn]))

    @jsii.member(jsii_name="fromOrganizationArn")
    @builtins.classmethod
    def from_organization_arn(cls, arn: builtins.str) -> "SharedPrincipal":
        '''
        :param arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedPrincipal.from_organization_arn)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast("SharedPrincipal", jsii.sinvoke(cls, "fromOrganizationArn", [arn]))

    @jsii.member(jsii_name="fromRole")
    @builtins.classmethod
    def from_role(cls, role: aws_cdk.aws_iam.IRole) -> "SharedPrincipal":
        '''
        :param role: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedPrincipal.from_role)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast("SharedPrincipal", jsii.sinvoke(cls, "fromRole", [role]))

    @jsii.member(jsii_name="fromStage")
    @builtins.classmethod
    def from_stage(cls, stage: aws_cdk.Stage) -> "SharedPrincipal":
        '''
        :param stage: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedPrincipal.from_stage)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast("SharedPrincipal", jsii.sinvoke(cls, "fromStage", [stage]))

    @jsii.member(jsii_name="fromUser")
    @builtins.classmethod
    def from_user(cls, user: aws_cdk.aws_iam.IUser) -> "SharedPrincipal":
        '''
        :param user: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedPrincipal.from_user)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast("SharedPrincipal", jsii.sinvoke(cls, "fromUser", [user]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> builtins.str:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedPrincipal.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(builtins.str, jsii.invoke(self, "bind", [_scope]))


@jsii.implements(ISharedResource)
class SharedResource(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ram.SharedResource",
):
    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(cls, arn: builtins.str) -> "SharedResource":
        '''
        :param arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedResource.from_arn)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast("SharedResource", jsii.sinvoke(cls, "fromArn", [arn]))

    @jsii.member(jsii_name="fromProject")
    @builtins.classmethod
    def from_project(cls, project: aws_cdk.aws_codebuild.IProject) -> "SharedResource":
        '''
        :param project: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedResource.from_project)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast("SharedResource", jsii.sinvoke(cls, "fromProject", [project]))

    @jsii.member(jsii_name="fromSubnet")
    @builtins.classmethod
    def from_subnet(cls, subnet: aws_cdk.aws_ec2.ISubnet) -> "SharedResource":
        '''
        :param subnet: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedResource.from_subnet)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        return typing.cast("SharedResource", jsii.sinvoke(cls, "fromSubnet", [subnet]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> builtins.str:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SharedResource.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(builtins.str, jsii.invoke(self, "bind", [_scope]))


__all__ = [
    "ISharedPrincipal",
    "ISharedResource",
    "ResourceShare",
    "ResourceShareProps",
    "SharedPrincipal",
    "SharedResource",
]

publication.publish()
