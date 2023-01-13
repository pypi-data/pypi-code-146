'''
<!-- A markdown formed message explaining we are deprecating this package and pointing to the new one. -->

# Deprecation Notice

Current package is deprecated and will not be maintained anymore. The implementation has been moved to leverage the new [AWS Landing Zone Accelerator solution](https://aws.amazon.com/solutions/implementations/landing-zone-accelerator-on-aws/) ([github](https://github.com/awslabs/landing-zone-accelerator-on-aws)).

# AWS Bootstrap Kit Overview  [![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/kolomied/awesome-cdk) ![badge npm version](https://img.shields.io/npm/v/aws-bootstrap-kit/latest)

This is a strongly opinionated CDK set of constructs built for companies looking to follow AWS best practices on Day 1 while setting their development and deployment environment on AWS.

Let's start small but with potential for future growth without adding tech debt.

## Getting started

Check our [examples repo](https://github.com/aws-samples/aws-bootstrap-kit-examples)

## Constructs

As of today we expose only one global package which expose a set of stacks and constructs to help you get started properly on AWS.

## Usage

1. install

   ```
   npm install aws-bootstrap-kit
   ```
2. Check the [Examples](https://github.com/aws-samples/aws-bootstrap-kit-examples) and [API Doc](./API.md) for more details

## Contributing

Check [CONTRIBUTING.md](./CONTRIBUTING.md))
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import constructs as _constructs_77d1e7e8


class Account(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-bootstrap-kit.Account",
):
    '''An AWS Account.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        account_props: "IAccountProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account_props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6b271d2a966792fd809e5ccc15702fc933cff39c6aafc3296e483b8816e34c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument account_props", value=account_props, expected_type=type_hints["account_props"])
        jsii.create(self.__class__, self, [scope, id, account_props])

    @jsii.member(jsii_name="registerAsDelegatedAdministrator")
    def register_as_delegated_administrator(
        self,
        account_id: builtins.str,
        service_principal: builtins.str,
    ) -> None:
        '''
        :param account_id: -
        :param service_principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa6c386ffa4f9813d16a0cfc9b593d6080edf42d85c118ef8cf80a481dc184a)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument service_principal", value=service_principal, expected_type=type_hints["service_principal"])
        return typing.cast(None, jsii.invoke(self, "registerAsDelegatedAdministrator", [account_id, service_principal]))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        '''Constructor.'''
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @builtins.property
    @jsii.member(jsii_name="accountStageName")
    def account_stage_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountStageName"))

    @builtins.property
    @jsii.member(jsii_name="accountStageOrder")
    def account_stage_order(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountStageOrder"))


@jsii.data_type(
    jsii_type="aws-bootstrap-kit.AccountSpec",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "email": "email",
        "existing_account_id": "existingAccountId",
        "hosted_services": "hostedServices",
        "removal_policy": "removalPolicy",
        "stage_name": "stageName",
        "stage_order": "stageOrder",
        "type": "type",
    },
)
class AccountSpec:
    def __init__(
        self,
        *,
        name: builtins.str,
        email: typing.Optional[builtins.str] = None,
        existing_account_id: typing.Optional[builtins.str] = None,
        hosted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        stage_name: typing.Optional[builtins.str] = None,
        stage_order: typing.Optional[jsii.Number] = None,
        type: typing.Optional["AccountType"] = None,
    ) -> None:
        '''AWS Account input details.

        :param name: The name of the AWS account.
        :param email: The email associated to the AWS account.
        :param existing_account_id: The (optional) id of the account to reuse, instead of creating a new account.
        :param hosted_services: List of your services that will be hosted in this account. Set it to [ALL] if you don't plan to have dedicated account for each service.
        :param removal_policy: RemovalPolicy of the account (wether it must be retained or destroyed). See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html#aws-attribute-deletionpolicy-options. As an account cannot be deleted, RETAIN is the default value. If you choose DESTROY instead (default behavior of CloudFormation), the stack deletion will fail and you will have to manually remove the account from the organization before retrying to delete the stack: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_remove.html Note that existing accounts (when using ``existingAccountId``) are retained whatever the removalPolicy is. Default: RemovalPolicy.RETAIN
        :param stage_name: The (optional) Stage name to be used in CI/CD pipeline.
        :param stage_order: The (optional) Stage deployment order.
        :param type: The account type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1187de7b8a4ac0668c6ffb7be332d1ff7fc2d933d539e94709422023db6c84)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument existing_account_id", value=existing_account_id, expected_type=type_hints["existing_account_id"])
            check_type(argname="argument hosted_services", value=hosted_services, expected_type=type_hints["hosted_services"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument stage_order", value=stage_order, expected_type=type_hints["stage_order"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if email is not None:
            self._values["email"] = email
        if existing_account_id is not None:
            self._values["existing_account_id"] = existing_account_id
        if hosted_services is not None:
            self._values["hosted_services"] = hosted_services
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if stage_order is not None:
            self._values["stage_order"] = stage_order
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the AWS account.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''The email associated to the AWS account.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_account_id(self) -> typing.Optional[builtins.str]:
        '''The (optional) id of the account to reuse, instead of creating a new account.'''
        result = self._values.get("existing_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of your services that will be hosted in this account.

        Set it to [ALL] if you don't plan to have dedicated account for each service.
        '''
        result = self._values.get("hosted_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''RemovalPolicy of the account (wether it must be retained or destroyed). See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html#aws-attribute-deletionpolicy-options.

        As an account cannot be deleted, RETAIN is the default value.

        If you choose DESTROY instead (default behavior of CloudFormation), the stack deletion will fail and
        you will have to manually remove the account from the organization before retrying to delete the stack:
        https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_remove.html

        Note that existing accounts (when using ``existingAccountId``) are retained whatever the removalPolicy is.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''The (optional) Stage name to be used in CI/CD pipeline.'''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_order(self) -> typing.Optional[jsii.Number]:
        '''The (optional) Stage deployment order.'''
        result = self._values.get("stage_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional["AccountType"]:
        '''The account type.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional["AccountType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-bootstrap-kit.AccountType")
class AccountType(enum.Enum):
    '''The type of the AWS account.'''

    CICD = "CICD"
    '''The account used to deploy CI/CD pipelines (See `here <https://cs.github.com/?scopeName=bk&scope=repo%3Aawslabs%2Faws-bootstrap-kit&q=AccountType.CICD>`_ for internal usage).'''
    STAGE = "STAGE"
    '''Accounts which will be used to deploy Stage environments (staging/prod ...). (See `here <https://cs.github.com/?scopeName=bk&scope=repo%3Aawslabs%2Faws-bootstrap-kit&q=AccountType.STAGE>`_ for internal usage).'''
    PLAYGROUND = "PLAYGROUND"
    '''Sandbox accounts dedicated to developers work.'''


class AwsOrganizationsStack(
    _aws_cdk_ceddda9d.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-bootstrap-kit.AwsOrganizationsStack",
):
    '''A Stack creating the Software Development Life Cycle (SDLC) Organization.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        email: builtins.str,
        nested_ou: typing.Sequence[typing.Union["OUSpec", typing.Dict[builtins.str, typing.Any]]],
        existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
        force_email_verification: typing.Optional[builtins.bool] = None,
        root_hosted_zone_dns_name: typing.Optional[builtins.str] = None,
        third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param email: (experimental) Email address of the Root account.
        :param nested_ou: (experimental) Specification of the sub Organizational Unit.
        :param existing_root_hosted_zone_id: (experimental) The (optional) existing root hosted zone id to use instead of creating one.
        :param force_email_verification: (experimental) Enable Email Verification Process.
        :param root_hosted_zone_dns_name: (experimental) The main DNS domain name to manage.
        :param third_party_provider_dns_used: (experimental) A boolean used to decide if domain should be requested through this delpoyment or if already registered through a third party.
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d36993711d292d7e86347f03bd97ddaea3cad46d042ebac9abdb7f6d1b8d5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsOrganizationsStackProps(
            email=email,
            nested_ou=nested_ou,
            existing_root_hosted_zone_id=existing_root_hosted_zone_id,
            force_email_verification=force_email_verification,
            root_hosted_zone_dns_name=root_hosted_zone_dns_name,
            third_party_provider_dns_used=third_party_provider_dns_used,
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            permissions_boundary=permissions_boundary,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="rootDns")
    def root_dns(self) -> typing.Optional["RootDns"]:
        return typing.cast(typing.Optional["RootDns"], jsii.get(self, "rootDns"))


@jsii.data_type(
    jsii_type="aws-bootstrap-kit.AwsOrganizationsStackProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.StackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "cross_region_references": "crossRegionReferences",
        "description": "description",
        "env": "env",
        "permissions_boundary": "permissionsBoundary",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "email": "email",
        "nested_ou": "nestedOU",
        "existing_root_hosted_zone_id": "existingRootHostedZoneId",
        "force_email_verification": "forceEmailVerification",
        "root_hosted_zone_dns_name": "rootHostedZoneDNSName",
        "third_party_provider_dns_used": "thirdPartyProviderDNSUsed",
    },
)
class AwsOrganizationsStackProps(_aws_cdk_ceddda9d.StackProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        email: builtins.str,
        nested_ou: typing.Sequence[typing.Union["OUSpec", typing.Dict[builtins.str, typing.Any]]],
        existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
        force_email_verification: typing.Optional[builtins.bool] = None,
        root_hosted_zone_dns_name: typing.Optional[builtins.str] = None,
        third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for AWS SDLC Organizations Stack.

        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param email: (experimental) Email address of the Root account.
        :param nested_ou: (experimental) Specification of the sub Organizational Unit.
        :param existing_root_hosted_zone_id: (experimental) The (optional) existing root hosted zone id to use instead of creating one.
        :param force_email_verification: (experimental) Enable Email Verification Process.
        :param root_hosted_zone_dns_name: (experimental) The main DNS domain name to manage.
        :param third_party_provider_dns_used: (experimental) A boolean used to decide if domain should be requested through this delpoyment or if already registered through a third party.

        :stability: experimental
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e7fb937239e5869b908a89d9a07947294ce0420306441bbb4d369ef489f80d)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument cross_region_references", value=cross_region_references, expected_type=type_hints["cross_region_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument nested_ou", value=nested_ou, expected_type=type_hints["nested_ou"])
            check_type(argname="argument existing_root_hosted_zone_id", value=existing_root_hosted_zone_id, expected_type=type_hints["existing_root_hosted_zone_id"])
            check_type(argname="argument force_email_verification", value=force_email_verification, expected_type=type_hints["force_email_verification"])
            check_type(argname="argument root_hosted_zone_dns_name", value=root_hosted_zone_dns_name, expected_type=type_hints["root_hosted_zone_dns_name"])
            check_type(argname="argument third_party_provider_dns_used", value=third_party_provider_dns_used, expected_type=type_hints["third_party_provider_dns_used"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
            "nested_ou": nested_ou,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if cross_region_references is not None:
            self._values["cross_region_references"] = cross_region_references
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if existing_root_hosted_zone_id is not None:
            self._values["existing_root_hosted_zone_id"] = existing_root_hosted_zone_id
        if force_email_verification is not None:
            self._values["force_email_verification"] = force_email_verification
        if root_hosted_zone_dns_name is not None:
            self._values["root_hosted_zone_dns_name"] = root_hosted_zone_dns_name
        if third_party_provider_dns_used is not None:
            self._values["third_party_provider_dns_used"] = third_party_provider_dns_used

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_references(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to allow native cross region stack references.

        Enabling this will create a CloudFormation custom resource
        in both the producing stack and consuming stack in order to perform the export/import

        This feature is currently experimental

        :default: false
        '''
        result = self._values.get("cross_region_references")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            // Use a concrete account and region to deploy this stack to:
            // `.account` and `.region` will simply return these values.
            new Stack(app, 'Stack1', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              },
            });
            
            // Use the CLI's current credentials to determine the target environment:
            // `.account` and `.region` will reflect the account+region the CLI
            // is configured to use (based on the user CLI credentials)
            new Stack(app, 'Stack2', {
              env: {
                account: process.env.CDK_DEFAULT_ACCOUNT,
                region: process.env.CDK_DEFAULT_REGION
              },
            });
            
            // Define multiple stacks stage associated with an environment
            const myStage = new Stage(app, 'MyStage', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              }
            });
            
            // both of these stacks will use the stage's account/region:
            // `.account` and `.region` will resolve to the concrete values as above
            new MyStack(myStage, 'Stack1');
            new YourStack(myStage, 'Stack2');
            
            // Define an environment-agnostic stack:
            // `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            // which will only resolve to actual values by CloudFormation during deployment.
            new MyStack(app, 'Stack1');
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary]:
        '''Options for applying a permissions boundary to all IAM Roles and Users created within this Stage.

        :default: - no permissions boundary is applied
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def email(self) -> builtins.str:
        '''(experimental) Email address of the Root account.

        :stability: experimental
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nested_ou(self) -> typing.List["OUSpec"]:
        '''(experimental) Specification of the sub Organizational Unit.

        :stability: experimental
        '''
        result = self._values.get("nested_ou")
        assert result is not None, "Required property 'nested_ou' is missing"
        return typing.cast(typing.List["OUSpec"], result)

    @builtins.property
    def existing_root_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The (optional) existing root hosted zone id to use instead of creating one.

        :stability: experimental
        '''
        result = self._values.get("existing_root_hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_email_verification(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable Email Verification Process.

        :stability: experimental
        '''
        result = self._values.get("force_email_verification")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def root_hosted_zone_dns_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The main DNS domain name to manage.

        :stability: experimental
        '''
        result = self._values.get("root_hosted_zone_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def third_party_provider_dns_used(self) -> typing.Optional[builtins.bool]:
        '''(experimental) A boolean used to decide if domain should be requested through this delpoyment or if already registered through a third party.

        :stability: experimental
        '''
        result = self._values.get("third_party_provider_dns_used")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsOrganizationsStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CrossAccountDNSDelegator(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-bootstrap-kit.CrossAccountDNSDelegator",
):
    '''TODO: propose this to fix https://github.com/aws/aws-cdk/issues/8776 High-level construct that creates: 1. A public hosted zone in the current account 2. A record name in the hosted zone id of target account.

    Usage:
    Create a role with the following permission:
    {
    "Sid": "VisualEditor0",
    "Effect": "Allow",
    "Action": [
    "route53:GetHostedZone",
    "route53:ChangeResourceRecordSets"
    ],
    "Resource": "arn:aws:route53:::hostedzone/ZXXXXXXXXX"
    }

    Then use the construct like this:

    const crossAccountDNSDelegatorProps: ICrossAccountDNSDelegatorProps = {
    targetAccount: '1234567890',
    targetRoleToAssume: 'DelegateRecordUpdateRoleInThatAccount',
    targetHostedZoneId: 'ZXXXXXXXXX',
    zoneName: 'subdomain.mydomain.com',
    };

    new CrossAccountDNSDelegator(this, 'CrossAccountDNSDelegatorStack', crossAccountDNSDelegatorProps);
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "ICrossAccountDNSDelegatorProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388187bfc53a0e4fed918e7f281e4daf763f0811f7bc03ed16dc63858345dd60)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="hostedZone")
    def hosted_zone(self) -> _aws_cdk_aws_route53_ceddda9d.HostedZone:
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.HostedZone, jsii.get(self, "hostedZone"))


@jsii.interface(jsii_type="aws-bootstrap-kit.IAccountProps")
class IAccountProps(typing_extensions.Protocol):
    '''Properties of an AWS account.'''

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        '''The email to use to create the AWS account.'''
        ...

    @email.setter
    def email(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the AWS Account.'''
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="hostedServices")
    def hosted_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of your services that will be hosted in this account.

        Set it to [ALL] if you don't plan to have dedicated account for each service.
        '''
        ...

    @hosted_services.setter
    def hosted_services(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[builtins.str]:
        '''The AWS account Id.'''
        ...

    @id.setter
    def id(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parentOrganizationalUnitId")
    def parent_organizational_unit_id(self) -> typing.Optional[builtins.str]:
        '''The potential Organizational Unit Id the account should be placed in.'''
        ...

    @parent_organizational_unit_id.setter
    def parent_organizational_unit_id(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parentOrganizationalUnitName")
    def parent_organizational_unit_name(self) -> typing.Optional[builtins.str]:
        '''The potential Organizational Unit Name the account should be placed in.'''
        ...

    @parent_organizational_unit_name.setter
    def parent_organizational_unit_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="removalPolicy")
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''RemovalPolicy of the account.

        See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html#aws-attribute-deletionpolicy-options

        :default: RemovalPolicy.RETAIN
        '''
        ...

    @removal_policy.setter
    def removal_policy(
        self,
        value: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''The (optional) Stage name to be used in CI/CD pipeline.'''
        ...

    @stage_name.setter
    def stage_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="stageOrder")
    def stage_order(self) -> typing.Optional[jsii.Number]:
        '''The (optional) Stage deployment order.'''
        ...

    @stage_order.setter
    def stage_order(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[AccountType]:
        '''The account type.'''
        ...

    @type.setter
    def type(self, value: typing.Optional[AccountType]) -> None:
        ...


class _IAccountPropsProxy:
    '''Properties of an AWS account.'''

    __jsii_type__: typing.ClassVar[str] = "aws-bootstrap-kit.IAccountProps"

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        '''The email to use to create the AWS account.'''
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16149943d489dc69493bd96260ef738a1fbdadbb11245c5445fb1873d97f3585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the AWS Account.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2731b11dbd6f6dd8789d13fb6f301c433c87e07df449998e0e197f8e3cefc671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="hostedServices")
    def hosted_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of your services that will be hosted in this account.

        Set it to [ALL] if you don't plan to have dedicated account for each service.
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostedServices"))

    @hosted_services.setter
    def hosted_services(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f687f2fa4b38b57b917848dddf3b8c8a1b8d0b45ae79db8be2047bfd9a0a6f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostedServices", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[builtins.str]:
        '''The AWS account Id.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "id"))

    @id.setter
    def id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9fb90bc34c7c62f4ecf24fc215343b062fe2bc8c1368de3b9b0691664afca4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="parentOrganizationalUnitId")
    def parent_organizational_unit_id(self) -> typing.Optional[builtins.str]:
        '''The potential Organizational Unit Id the account should be placed in.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentOrganizationalUnitId"))

    @parent_organizational_unit_id.setter
    def parent_organizational_unit_id(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96b03d906935514dfbc4952388e4ca869fb4de7737c0c1da2718b90415bf61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentOrganizationalUnitId", value)

    @builtins.property
    @jsii.member(jsii_name="parentOrganizationalUnitName")
    def parent_organizational_unit_name(self) -> typing.Optional[builtins.str]:
        '''The potential Organizational Unit Name the account should be placed in.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentOrganizationalUnitName"))

    @parent_organizational_unit_name.setter
    def parent_organizational_unit_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce017ddd407008a18ddd2bf79a7a0a1ee134527f6b2cbe986356930300726e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentOrganizationalUnitName", value)

    @builtins.property
    @jsii.member(jsii_name="removalPolicy")
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''RemovalPolicy of the account.

        See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html#aws-attribute-deletionpolicy-options

        :default: RemovalPolicy.RETAIN
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], jsii.get(self, "removalPolicy"))

    @removal_policy.setter
    def removal_policy(
        self,
        value: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416da4ae894ed346f495979a1dd05337a6d502b8c5376e6b5762b138a01b5620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removalPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''The (optional) Stage name to be used in CI/CD pipeline.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageName"))

    @stage_name.setter
    def stage_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56dc2dca4f8d7940c8275d49ea1bef5b99f66c9f8ff6b58db5dbee6b952a22de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="stageOrder")
    def stage_order(self) -> typing.Optional[jsii.Number]:
        '''The (optional) Stage deployment order.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stageOrder"))

    @stage_order.setter
    def stage_order(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a84c6a97044fe00cd079b9c4cd77f6c58bbd12d7a77cfb8184fb1ec205590a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageOrder", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[AccountType]:
        '''The account type.'''
        return typing.cast(typing.Optional[AccountType], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[AccountType]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2280598738c89c91fc933245fd88baa4c3ec3f7cfc575fce44c5a1ffab132ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAccountProps).__jsii_proxy_class__ = lambda : _IAccountPropsProxy


@jsii.interface(jsii_type="aws-bootstrap-kit.ICrossAccountDNSDelegatorProps")
class ICrossAccountDNSDelegatorProps(typing_extensions.Protocol):
    '''Properties to create delegated subzone of a zone hosted in a different account.'''

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> builtins.str:
        '''The sub zone name to be created.'''
        ...

    @zone_name.setter
    def zone_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="targetAccount")
    def target_account(self) -> typing.Optional[builtins.str]:
        '''The Account hosting the parent zone Optional since can be resolved if the system has been setup with aws-bootstrap-kit.'''
        ...

    @target_account.setter
    def target_account(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="targetHostedZoneId")
    def target_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''The parent zone Id to add the sub zone delegation NS record to Optional since can be resolved if the system has been setup with aws-bootstrap-kit.'''
        ...

    @target_hosted_zone_id.setter
    def target_hosted_zone_id(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="targetRoleToAssume")
    def target_role_to_assume(self) -> typing.Optional[builtins.str]:
        '''The role to Assume in the parent zone's account which has permissions to update the parent zone Optional since can be resolved if the system has been setup with aws-bootstrap-kit.'''
        ...

    @target_role_to_assume.setter
    def target_role_to_assume(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ICrossAccountDNSDelegatorPropsProxy:
    '''Properties to create delegated subzone of a zone hosted in a different account.'''

    __jsii_type__: typing.ClassVar[str] = "aws-bootstrap-kit.ICrossAccountDNSDelegatorProps"

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> builtins.str:
        '''The sub zone name to be created.'''
        return typing.cast(builtins.str, jsii.get(self, "zoneName"))

    @zone_name.setter
    def zone_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426fe01454781869fb8f3ecad556b52d967185ed879075e3d35e73a2c876c0ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneName", value)

    @builtins.property
    @jsii.member(jsii_name="targetAccount")
    def target_account(self) -> typing.Optional[builtins.str]:
        '''The Account hosting the parent zone Optional since can be resolved if the system has been setup with aws-bootstrap-kit.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetAccount"))

    @target_account.setter
    def target_account(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc4f5cce10ea087168e8e3969d4f0d19d6298fa6eee784bc753d7edb5237010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetAccount", value)

    @builtins.property
    @jsii.member(jsii_name="targetHostedZoneId")
    def target_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''The parent zone Id to add the sub zone delegation NS record to Optional since can be resolved if the system has been setup with aws-bootstrap-kit.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetHostedZoneId"))

    @target_hosted_zone_id.setter
    def target_hosted_zone_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e846dd48ee45c1c60a95e8d48339e310f6fa76c1177b939c1e8ae262fd0d0ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetHostedZoneId", value)

    @builtins.property
    @jsii.member(jsii_name="targetRoleToAssume")
    def target_role_to_assume(self) -> typing.Optional[builtins.str]:
        '''The role to Assume in the parent zone's account which has permissions to update the parent zone Optional since can be resolved if the system has been setup with aws-bootstrap-kit.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRoleToAssume"))

    @target_role_to_assume.setter
    def target_role_to_assume(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e050d9d7eb3f13ec874d510496e4510b36186b1719014696c2ba291ea57e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRoleToAssume", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICrossAccountDNSDelegatorProps).__jsii_proxy_class__ = lambda : _ICrossAccountDNSDelegatorPropsProxy


@jsii.data_type(
    jsii_type="aws-bootstrap-kit.OUSpec",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "accounts": "accounts", "nested_ou": "nestedOU"},
)
class OUSpec:
    def __init__(
        self,
        *,
        name: builtins.str,
        accounts: typing.Optional[typing.Sequence[typing.Union[AccountSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
        nested_ou: typing.Optional[typing.Sequence[typing.Union["OUSpec", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Organizational Unit Input details.

        :param name: Name of the Organizational Unit.
        :param accounts: Accounts' specification inside in this Organizational Unit.
        :param nested_ou: Specification of sub Organizational Unit.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d497457fa58915b6a59f96540cba2d43001a8afc8ea2d26bb071471e5aec70f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument nested_ou", value=nested_ou, expected_type=type_hints["nested_ou"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if accounts is not None:
            self._values["accounts"] = accounts
        if nested_ou is not None:
            self._values["nested_ou"] = nested_ou

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Organizational Unit.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accounts(self) -> typing.Optional[typing.List[AccountSpec]]:
        '''Accounts' specification inside in this Organizational Unit.'''
        result = self._values.get("accounts")
        return typing.cast(typing.Optional[typing.List[AccountSpec]], result)

    @builtins.property
    def nested_ou(self) -> typing.Optional[typing.List["OUSpec"]]:
        '''Specification of sub Organizational Unit.'''
        result = self._values.get("nested_ou")
        return typing.cast(typing.Optional[typing.List["OUSpec"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OUSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RootDns(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-bootstrap-kit.RootDns",
):
    '''A class creating the main hosted zone and a role assumable by stages account to be able to set sub domain delegation.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        root_hosted_zone_dns_name: builtins.str,
        stages_accounts: typing.Sequence[Account],
        existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
        third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param root_hosted_zone_dns_name: The top level domain name.
        :param stages_accounts: The stages Accounts taht will need their subzone delegation.
        :param existing_root_hosted_zone_id: The (optional) existing root hosted zone id to use instead of creating one.
        :param third_party_provider_dns_used: A boolean indicating if Domain name has already been registered to a third party or if you want this contruct to create it (the latter is not yet supported).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2863301e1d3299de1f3e811d36b17c9149d0d2c93d27519c7db01cf099321bef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RootDnsProps(
            root_hosted_zone_dns_name=root_hosted_zone_dns_name,
            stages_accounts=stages_accounts,
            existing_root_hosted_zone_id=existing_root_hosted_zone_id,
            third_party_provider_dns_used=third_party_provider_dns_used,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createDNSAutoUpdateRole")
    def create_dns_auto_update_role(
        self,
        account: Account,
        stage_sub_zone: _aws_cdk_aws_route53_ceddda9d.HostedZone,
    ) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :param account: -
        :param stage_sub_zone: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46dbae6b1bbc4cc12324101b3368e7f71d9da7d3e095cba266165288c1b3a32c)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument stage_sub_zone", value=stage_sub_zone, expected_type=type_hints["stage_sub_zone"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.invoke(self, "createDNSAutoUpdateRole", [account, stage_sub_zone]))

    @jsii.member(jsii_name="createRootHostedZone")
    def create_root_hosted_zone(
        self,
        *,
        root_hosted_zone_dns_name: builtins.str,
        stages_accounts: typing.Sequence[Account],
        existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
        third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        '''
        :param root_hosted_zone_dns_name: The top level domain name.
        :param stages_accounts: The stages Accounts taht will need their subzone delegation.
        :param existing_root_hosted_zone_id: The (optional) existing root hosted zone id to use instead of creating one.
        :param third_party_provider_dns_used: A boolean indicating if Domain name has already been registered to a third party or if you want this contruct to create it (the latter is not yet supported).
        '''
        props = RootDnsProps(
            root_hosted_zone_dns_name=root_hosted_zone_dns_name,
            stages_accounts=stages_accounts,
            existing_root_hosted_zone_id=existing_root_hosted_zone_id,
            third_party_provider_dns_used=third_party_provider_dns_used,
        )

        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, jsii.invoke(self, "createRootHostedZone", [props]))

    @jsii.member(jsii_name="createStageSubZone")
    def create_stage_sub_zone(
        self,
        account: Account,
        root_hosted_zone_dns_name: builtins.str,
    ) -> _aws_cdk_aws_route53_ceddda9d.HostedZone:
        '''
        :param account: -
        :param root_hosted_zone_dns_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af5386fac5856bdafe6136d5dda4a54f90083458175d35fbe920e1324fb386d)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument root_hosted_zone_dns_name", value=root_hosted_zone_dns_name, expected_type=type_hints["root_hosted_zone_dns_name"])
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.HostedZone, jsii.invoke(self, "createStageSubZone", [account, root_hosted_zone_dns_name]))

    @builtins.property
    @jsii.member(jsii_name="rootHostedZone")
    def root_hosted_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, jsii.get(self, "rootHostedZone"))

    @builtins.property
    @jsii.member(jsii_name="stagesHostedZones")
    def stages_hosted_zones(
        self,
    ) -> typing.List[_aws_cdk_aws_route53_ceddda9d.HostedZone]:
        return typing.cast(typing.List[_aws_cdk_aws_route53_ceddda9d.HostedZone], jsii.get(self, "stagesHostedZones"))


@jsii.data_type(
    jsii_type="aws-bootstrap-kit.RootDnsProps",
    jsii_struct_bases=[],
    name_mapping={
        "root_hosted_zone_dns_name": "rootHostedZoneDNSName",
        "stages_accounts": "stagesAccounts",
        "existing_root_hosted_zone_id": "existingRootHostedZoneId",
        "third_party_provider_dns_used": "thirdPartyProviderDNSUsed",
    },
)
class RootDnsProps:
    def __init__(
        self,
        *,
        root_hosted_zone_dns_name: builtins.str,
        stages_accounts: typing.Sequence[Account],
        existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
        third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties for RootDns.

        :param root_hosted_zone_dns_name: The top level domain name.
        :param stages_accounts: The stages Accounts taht will need their subzone delegation.
        :param existing_root_hosted_zone_id: The (optional) existing root hosted zone id to use instead of creating one.
        :param third_party_provider_dns_used: A boolean indicating if Domain name has already been registered to a third party or if you want this contruct to create it (the latter is not yet supported).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49479bf1d6cc21965449de9df9e200ccd5d58e39bb1707d93b2b2183a35b9d7)
            check_type(argname="argument root_hosted_zone_dns_name", value=root_hosted_zone_dns_name, expected_type=type_hints["root_hosted_zone_dns_name"])
            check_type(argname="argument stages_accounts", value=stages_accounts, expected_type=type_hints["stages_accounts"])
            check_type(argname="argument existing_root_hosted_zone_id", value=existing_root_hosted_zone_id, expected_type=type_hints["existing_root_hosted_zone_id"])
            check_type(argname="argument third_party_provider_dns_used", value=third_party_provider_dns_used, expected_type=type_hints["third_party_provider_dns_used"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "root_hosted_zone_dns_name": root_hosted_zone_dns_name,
            "stages_accounts": stages_accounts,
        }
        if existing_root_hosted_zone_id is not None:
            self._values["existing_root_hosted_zone_id"] = existing_root_hosted_zone_id
        if third_party_provider_dns_used is not None:
            self._values["third_party_provider_dns_used"] = third_party_provider_dns_used

    @builtins.property
    def root_hosted_zone_dns_name(self) -> builtins.str:
        '''The top level domain name.'''
        result = self._values.get("root_hosted_zone_dns_name")
        assert result is not None, "Required property 'root_hosted_zone_dns_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stages_accounts(self) -> typing.List[Account]:
        '''The stages Accounts taht will need their subzone delegation.'''
        result = self._values.get("stages_accounts")
        assert result is not None, "Required property 'stages_accounts' is missing"
        return typing.cast(typing.List[Account], result)

    @builtins.property
    def existing_root_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''The (optional) existing root hosted zone id to use instead of creating one.'''
        result = self._values.get("existing_root_hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def third_party_provider_dns_used(self) -> typing.Optional[builtins.bool]:
        '''A boolean indicating if Domain name has already been registered to a third party or if you want this contruct to create it (the latter is not yet supported).'''
        result = self._values.get("third_party_provider_dns_used")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RootDnsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecureRootUser(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-bootstrap-kit.SecureRootUser",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        notification_email: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param notification_email: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de7d6ca9e23addb1247fcc7e599b89a43a3d1754edd5ced482dbed812c6db34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_email", value=notification_email, expected_type=type_hints["notification_email"])
        jsii.create(self.__class__, self, [scope, id, notification_email])


class ValidateEmail(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-bootstrap-kit.ValidateEmail",
):
    '''Email Validation.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        email: builtins.str,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Constructor.

        :param scope: The parent Construct instantiating this construct.
        :param id: This instance name.
        :param email: Email address of the Root account.
        :param timeout: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfc3f111b12121b2a9eeb9480aa831ee4023994f3959bb20eaef065298fb6bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ValidateEmailProps(email=email, timeout=timeout)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-bootstrap-kit.ValidateEmailProps",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "timeout": "timeout"},
)
class ValidateEmailProps:
    def __init__(
        self,
        *,
        email: builtins.str,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Properties of ValidateEmail.

        :param email: Email address of the Root account.
        :param timeout: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796d6cbd24df93af4253b1290e6c54b7ceb3a067652d91d6a03794d48096e609)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def email(self) -> builtins.str:
        '''Email address of the Root account.'''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValidateEmailProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Account",
    "AccountSpec",
    "AccountType",
    "AwsOrganizationsStack",
    "AwsOrganizationsStackProps",
    "CrossAccountDNSDelegator",
    "IAccountProps",
    "ICrossAccountDNSDelegatorProps",
    "OUSpec",
    "RootDns",
    "RootDnsProps",
    "SecureRootUser",
    "ValidateEmail",
    "ValidateEmailProps",
]

publication.publish()

def _typecheckingstub__af6b271d2a966792fd809e5ccc15702fc933cff39c6aafc3296e483b8816e34c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    account_props: IAccountProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa6c386ffa4f9813d16a0cfc9b593d6080edf42d85c118ef8cf80a481dc184a(
    account_id: builtins.str,
    service_principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1187de7b8a4ac0668c6ffb7be332d1ff7fc2d933d539e94709422023db6c84(
    *,
    name: builtins.str,
    email: typing.Optional[builtins.str] = None,
    existing_account_id: typing.Optional[builtins.str] = None,
    hosted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    stage_name: typing.Optional[builtins.str] = None,
    stage_order: typing.Optional[jsii.Number] = None,
    type: typing.Optional[AccountType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d36993711d292d7e86347f03bd97ddaea3cad46d042ebac9abdb7f6d1b8d5c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    email: builtins.str,
    nested_ou: typing.Sequence[typing.Union[OUSpec, typing.Dict[builtins.str, typing.Any]]],
    existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
    force_email_verification: typing.Optional[builtins.bool] = None,
    root_hosted_zone_dns_name: typing.Optional[builtins.str] = None,
    third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e7fb937239e5869b908a89d9a07947294ce0420306441bbb4d369ef489f80d(
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    email: builtins.str,
    nested_ou: typing.Sequence[typing.Union[OUSpec, typing.Dict[builtins.str, typing.Any]]],
    existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
    force_email_verification: typing.Optional[builtins.bool] = None,
    root_hosted_zone_dns_name: typing.Optional[builtins.str] = None,
    third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388187bfc53a0e4fed918e7f281e4daf763f0811f7bc03ed16dc63858345dd60(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: ICrossAccountDNSDelegatorProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16149943d489dc69493bd96260ef738a1fbdadbb11245c5445fb1873d97f3585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2731b11dbd6f6dd8789d13fb6f301c433c87e07df449998e0e197f8e3cefc671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f687f2fa4b38b57b917848dddf3b8c8a1b8d0b45ae79db8be2047bfd9a0a6f64(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fb90bc34c7c62f4ecf24fc215343b062fe2bc8c1368de3b9b0691664afca4b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96b03d906935514dfbc4952388e4ca869fb4de7737c0c1da2718b90415bf61f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce017ddd407008a18ddd2bf79a7a0a1ee134527f6b2cbe986356930300726e3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416da4ae894ed346f495979a1dd05337a6d502b8c5376e6b5762b138a01b5620(
    value: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dc2dca4f8d7940c8275d49ea1bef5b99f66c9f8ff6b58db5dbee6b952a22de(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a84c6a97044fe00cd079b9c4cd77f6c58bbd12d7a77cfb8184fb1ec205590a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2280598738c89c91fc933245fd88baa4c3ec3f7cfc575fce44c5a1ffab132ff(
    value: typing.Optional[AccountType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426fe01454781869fb8f3ecad556b52d967185ed879075e3d35e73a2c876c0ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc4f5cce10ea087168e8e3969d4f0d19d6298fa6eee784bc753d7edb5237010(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e846dd48ee45c1c60a95e8d48339e310f6fa76c1177b939c1e8ae262fd0d0ada(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e050d9d7eb3f13ec874d510496e4510b36186b1719014696c2ba291ea57e7a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d497457fa58915b6a59f96540cba2d43001a8afc8ea2d26bb071471e5aec70f(
    *,
    name: builtins.str,
    accounts: typing.Optional[typing.Sequence[typing.Union[AccountSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
    nested_ou: typing.Optional[typing.Sequence[typing.Union[OUSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2863301e1d3299de1f3e811d36b17c9149d0d2c93d27519c7db01cf099321bef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    root_hosted_zone_dns_name: builtins.str,
    stages_accounts: typing.Sequence[Account],
    existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
    third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46dbae6b1bbc4cc12324101b3368e7f71d9da7d3e095cba266165288c1b3a32c(
    account: Account,
    stage_sub_zone: _aws_cdk_aws_route53_ceddda9d.HostedZone,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af5386fac5856bdafe6136d5dda4a54f90083458175d35fbe920e1324fb386d(
    account: Account,
    root_hosted_zone_dns_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49479bf1d6cc21965449de9df9e200ccd5d58e39bb1707d93b2b2183a35b9d7(
    *,
    root_hosted_zone_dns_name: builtins.str,
    stages_accounts: typing.Sequence[Account],
    existing_root_hosted_zone_id: typing.Optional[builtins.str] = None,
    third_party_provider_dns_used: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de7d6ca9e23addb1247fcc7e599b89a43a3d1754edd5ced482dbed812c6db34(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    notification_email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfc3f111b12121b2a9eeb9480aa831ee4023994f3959bb20eaef065298fb6bd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    email: builtins.str,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796d6cbd24df93af4253b1290e6c54b7ceb3a067652d91d6a03794d48096e609(
    *,
    email: builtins.str,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
