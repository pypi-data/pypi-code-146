'''
# AWS::RolesAnywhere Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_rolesanywhere as rolesanywhere
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for RolesAnywhere construct libraries](https://constructs.dev/search?q=rolesanywhere)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::RolesAnywhere resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RolesAnywhere.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::RolesAnywhere](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RolesAnywhere.html).

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
class CfnCRL(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-rolesanywhere.CfnCRL",
):
    '''A CloudFormation ``AWS::RolesAnywhere::CRL``.

    Creates a Crl.

    :cloudformationResource: AWS::RolesAnywhere::CRL
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_rolesanywhere as rolesanywhere
        
        cfn_cRL = rolesanywhere.CfnCRL(self, "MyCfnCRL",
            crl_data="crlData",
            enabled=False,
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trust_anchor_arn="trustAnchorArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        crl_data: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trust_anchor_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RolesAnywhere::CRL``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param crl_data: x509 v3 Certificate Revocation List to revoke auth for corresponding certificates presented in CreateSession operations.
        :param enabled: The enabled status of the resource.
        :param name: The customer specified name of the resource.
        :param tags: A list of Tags.
        :param trust_anchor_arn: The ARN of the TrustAnchor the certificate revocation list (CRL) will provide revocation for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f5127a6072e3e1594ed84e52ee329f0bec784663210b882365111bcb9d74c1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCRLProps(
            crl_data=crl_data,
            enabled=enabled,
            name=name,
            tags=tags,
            trust_anchor_arn=trust_anchor_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57745232024b81a7bb1d3b6309e92eb2b57e18d190b4f7b79d5efe0fbcd20c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1453dbfe2782a40ac1a42e90244804217bcefdbb157c124d04a2fba86404c021)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCrlId")
    def attr_crl_id(self) -> builtins.str:
        '''The unique primary identifier of the Crl.

        :cloudformationAttribute: CrlId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCrlId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="crlData")
    def crl_data(self) -> typing.Optional[builtins.str]:
        '''x509 v3 Certificate Revocation List to revoke auth for corresponding certificates presented in CreateSession operations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-crldata
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crlData"))

    @crl_data.setter
    def crl_data(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac2a0417b0966cae3171dc1f30922ee70d6d033d75a5944fa3c161bf241815f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crlData", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The enabled status of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5dd36764c4929bb8117db2f2886f48bef59cff15515ca943449ba13a386a4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The customer specified name of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f232a9f7129ce024864783b6e54b238dce6eec305747da4ed6e4dddacf1ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="trustAnchorArn")
    def trust_anchor_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the TrustAnchor the certificate revocation list (CRL) will provide revocation for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-trustanchorarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustAnchorArn"))

    @trust_anchor_arn.setter
    def trust_anchor_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a54775207bd13031efb15e0a837a922056023b06fc4872cb6d2fe831f3348e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustAnchorArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-rolesanywhere.CfnCRLProps",
    jsii_struct_bases=[],
    name_mapping={
        "crl_data": "crlData",
        "enabled": "enabled",
        "name": "name",
        "tags": "tags",
        "trust_anchor_arn": "trustAnchorArn",
    },
)
class CfnCRLProps:
    def __init__(
        self,
        *,
        crl_data: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trust_anchor_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCRL``.

        :param crl_data: x509 v3 Certificate Revocation List to revoke auth for corresponding certificates presented in CreateSession operations.
        :param enabled: The enabled status of the resource.
        :param name: The customer specified name of the resource.
        :param tags: A list of Tags.
        :param trust_anchor_arn: The ARN of the TrustAnchor the certificate revocation list (CRL) will provide revocation for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_rolesanywhere as rolesanywhere
            
            cfn_cRLProps = rolesanywhere.CfnCRLProps(
                crl_data="crlData",
                enabled=False,
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trust_anchor_arn="trustAnchorArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7213a68a2891838e5c133b3c0895cdabe1415dbe03f8c3ef8cae71574d42357e)
            check_type(argname="argument crl_data", value=crl_data, expected_type=type_hints["crl_data"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trust_anchor_arn", value=trust_anchor_arn, expected_type=type_hints["trust_anchor_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if crl_data is not None:
            self._values["crl_data"] = crl_data
        if enabled is not None:
            self._values["enabled"] = enabled
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if trust_anchor_arn is not None:
            self._values["trust_anchor_arn"] = trust_anchor_arn

    @builtins.property
    def crl_data(self) -> typing.Optional[builtins.str]:
        '''x509 v3 Certificate Revocation List to revoke auth for corresponding certificates presented in CreateSession operations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-crldata
        '''
        result = self._values.get("crl_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The enabled status of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The customer specified name of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def trust_anchor_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the TrustAnchor the certificate revocation list (CRL) will provide revocation for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-trustanchorarn
        '''
        result = self._values.get("trust_anchor_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCRLProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnProfile(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-rolesanywhere.CfnProfile",
):
    '''A CloudFormation ``AWS::RolesAnywhere::Profile``.

    Creates a Profile.

    :cloudformationResource: AWS::RolesAnywhere::Profile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_rolesanywhere as rolesanywhere
        
        cfn_profile = rolesanywhere.CfnProfile(self, "MyCfnProfile",
            duration_seconds=123,
            enabled=False,
            managed_policy_arns=["managedPolicyArns"],
            name="name",
            require_instance_properties=False,
            role_arns=["roleArns"],
            session_policy="sessionPolicy",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        duration_seconds: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        require_instance_properties: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RolesAnywhere::Profile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param duration_seconds: The number of seconds vended session credentials will be valid for.
        :param enabled: The enabled status of the resource.
        :param managed_policy_arns: A list of managed policy ARNs. Managed policies identified by this list will be applied to the vended session credentials.
        :param name: The customer specified name of the resource.
        :param require_instance_properties: Specifies whether instance properties are required in CreateSession requests with this profile.
        :param role_arns: A list of IAM role ARNs that can be assumed when this profile is specified in a CreateSession request.
        :param session_policy: A session policy that will applied to the trust boundary of the vended session credentials.
        :param tags: A list of Tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6806ee15cca56bda4267a22b759ed8375cd2e62db06437e7f09fada55005a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProfileProps(
            duration_seconds=duration_seconds,
            enabled=enabled,
            managed_policy_arns=managed_policy_arns,
            name=name,
            require_instance_properties=require_instance_properties,
            role_arns=role_arns,
            session_policy=session_policy,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce153bf3134dbba710a985eb2442ada7df6017ca5f6bd0dd8f53e470425671a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cc02f0e47776966423a52563a72de0d29aab0ad8adb1e7355ed108924b9d233)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileArn")
    def attr_profile_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ProfileArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileId")
    def attr_profile_id(self) -> builtins.str:
        '''The unique primary identifier of the Profile.

        :cloudformationAttribute: ProfileId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="durationSeconds")
    def duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds vended session credentials will be valid for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-durationseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationSeconds"))

    @duration_seconds.setter
    def duration_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074dbf3efe952e42283ffde79193facf80b79723a75d5014cd3b6415dcbc7aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The enabled status of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8af40145f48856b43419fd448c6d8600ca768f15d59172027f57763f6a48c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of managed policy ARNs.

        Managed policies identified by this list will be applied to the vended session credentials.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-managedpolicyarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "managedPolicyArns"))

    @managed_policy_arns.setter
    def managed_policy_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aefe2ad624ae5cf970333bbdfaf8c18ede4b858175bddef4bdf378de4e662b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The customer specified name of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f247d3c51644191eaec666b0a9d9a314cec1a8429887d9d0a6e6b7a40269408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="requireInstanceProperties")
    def require_instance_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether instance properties are required in CreateSession requests with this profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-requireinstanceproperties
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "requireInstanceProperties"))

    @require_instance_properties.setter
    def require_instance_properties(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa27d61e7c7f776e6f4a2967444d750b22d35d07301e48387a3982103c698e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireInstanceProperties", value)

    @builtins.property
    @jsii.member(jsii_name="roleArns")
    def role_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM role ARNs that can be assumed when this profile is specified in a CreateSession request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-rolearns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "roleArns"))

    @role_arns.setter
    def role_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44b61b11fdd9225ee855d6e3e295ff98a14b4378d514b0483bd7a83fa7fbad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArns", value)

    @builtins.property
    @jsii.member(jsii_name="sessionPolicy")
    def session_policy(self) -> typing.Optional[builtins.str]:
        '''A session policy that will applied to the trust boundary of the vended session credentials.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-sessionpolicy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionPolicy"))

    @session_policy.setter
    def session_policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186c9185f0e3d382d003898d6e137d4486b32d8fbf5677e0314503cf4d058485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionPolicy", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-rolesanywhere.CfnProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "duration_seconds": "durationSeconds",
        "enabled": "enabled",
        "managed_policy_arns": "managedPolicyArns",
        "name": "name",
        "require_instance_properties": "requireInstanceProperties",
        "role_arns": "roleArns",
        "session_policy": "sessionPolicy",
        "tags": "tags",
    },
)
class CfnProfileProps:
    def __init__(
        self,
        *,
        duration_seconds: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        require_instance_properties: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProfile``.

        :param duration_seconds: The number of seconds vended session credentials will be valid for.
        :param enabled: The enabled status of the resource.
        :param managed_policy_arns: A list of managed policy ARNs. Managed policies identified by this list will be applied to the vended session credentials.
        :param name: The customer specified name of the resource.
        :param require_instance_properties: Specifies whether instance properties are required in CreateSession requests with this profile.
        :param role_arns: A list of IAM role ARNs that can be assumed when this profile is specified in a CreateSession request.
        :param session_policy: A session policy that will applied to the trust boundary of the vended session credentials.
        :param tags: A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_rolesanywhere as rolesanywhere
            
            cfn_profile_props = rolesanywhere.CfnProfileProps(
                duration_seconds=123,
                enabled=False,
                managed_policy_arns=["managedPolicyArns"],
                name="name",
                require_instance_properties=False,
                role_arns=["roleArns"],
                session_policy="sessionPolicy",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68479953be44aa9e517847e17515e2e417b0906a41d1593d6e862765cc542971)
            check_type(argname="argument duration_seconds", value=duration_seconds, expected_type=type_hints["duration_seconds"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument require_instance_properties", value=require_instance_properties, expected_type=type_hints["require_instance_properties"])
            check_type(argname="argument role_arns", value=role_arns, expected_type=type_hints["role_arns"])
            check_type(argname="argument session_policy", value=session_policy, expected_type=type_hints["session_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if duration_seconds is not None:
            self._values["duration_seconds"] = duration_seconds
        if enabled is not None:
            self._values["enabled"] = enabled
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if name is not None:
            self._values["name"] = name
        if require_instance_properties is not None:
            self._values["require_instance_properties"] = require_instance_properties
        if role_arns is not None:
            self._values["role_arns"] = role_arns
        if session_policy is not None:
            self._values["session_policy"] = session_policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds vended session credentials will be valid for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-durationseconds
        '''
        result = self._values.get("duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The enabled status of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of managed policy ARNs.

        Managed policies identified by this list will be applied to the vended session credentials.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-managedpolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The customer specified name of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_instance_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether instance properties are required in CreateSession requests with this profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-requireinstanceproperties
        '''
        result = self._values.get("require_instance_properties")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def role_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM role ARNs that can be assumed when this profile is specified in a CreateSession request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-rolearns
        '''
        result = self._values.get("role_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_policy(self) -> typing.Optional[builtins.str]:
        '''A session policy that will applied to the trust boundary of the vended session credentials.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-sessionpolicy
        '''
        result = self._values.get("session_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnTrustAnchor(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-rolesanywhere.CfnTrustAnchor",
):
    '''A CloudFormation ``AWS::RolesAnywhere::TrustAnchor``.

    Creates a TrustAnchor.

    :cloudformationResource: AWS::RolesAnywhere::TrustAnchor
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_rolesanywhere as rolesanywhere
        
        cfn_trust_anchor = rolesanywhere.CfnTrustAnchor(self, "MyCfnTrustAnchor",
            enabled=False,
            name="name",
            source=rolesanywhere.CfnTrustAnchor.SourceProperty(
                source_data=rolesanywhere.CfnTrustAnchor.SourceDataProperty(
                    acm_pca_arn="acmPcaArn",
                    x509_certificate_data="x509CertificateData"
                ),
                source_type="sourceType"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTrustAnchor.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RolesAnywhere::TrustAnchor``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param enabled: Indicates whether the trust anchor is enabled.
        :param name: The name of the trust anchor.
        :param source: The trust anchor type and its related certificate data.
        :param tags: A list of tags to attach to the trust anchor.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6896e80f72d00d000494119ad365fe5d1d1b7020e2013f9e9b0d6323a75c949)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTrustAnchorProps(
            enabled=enabled, name=name, source=source, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8c29dd3eac7196a5ce9f905ba42b5ffe6b2951973715c23176171e7438c6ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__267ce50452d28a82d4fbbe6ecfdf6d51ccc17a2c41a247c219be70700b8abca3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrTrustAnchorArn")
    def attr_trust_anchor_arn(self) -> builtins.str:
        '''The ARN of the trust anchor.

        :cloudformationAttribute: TrustAnchorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTrustAnchorArn"))

    @builtins.property
    @jsii.member(jsii_name="attrTrustAnchorId")
    def attr_trust_anchor_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: TrustAnchorId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTrustAnchorId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of tags to attach to the trust anchor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether the trust anchor is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfc52bdcd353242b1cc3874b0ad92fd3241bc0a94166599dacfb27c12384623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the trust anchor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7737804f567c8e53cbf1fe4bdfda25aa66fa2e485937face7b9ff01d2010245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTrustAnchor.SourceProperty"]]:
        '''The trust anchor type and its related certificate data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-source
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTrustAnchor.SourceProperty"]], jsii.get(self, "source"))

    @source.setter
    def source(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTrustAnchor.SourceProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bed2153cb8af0544f782db5b3fe21582f9500bcb5f1c2f3ce9cb7721cba9455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-rolesanywhere.CfnTrustAnchor.SourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acm_pca_arn": "acmPcaArn",
            "x509_certificate_data": "x509CertificateData",
        },
    )
    class SourceDataProperty:
        def __init__(
            self,
            *,
            acm_pca_arn: typing.Optional[builtins.str] = None,
            x509_certificate_data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A union object representing the data field of the TrustAnchor depending on its type.

            :param acm_pca_arn: The root certificate of the AWS Private Certificate Authority specified by this ARN is used in trust validation for temporary credential requests. Included for trust anchors of type ``AWS_ACM_PCA`` .
            :param x509_certificate_data: The PEM-encoded data for the certificate anchor. Included for trust anchors of type ``CERTIFICATE_BUNDLE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-sourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_rolesanywhere as rolesanywhere
                
                source_data_property = rolesanywhere.CfnTrustAnchor.SourceDataProperty(
                    acm_pca_arn="acmPcaArn",
                    x509_certificate_data="x509CertificateData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__047566853c0f637ae8d56c48d17fcede72c704aa1cd6f955dbd6669d480e4be2)
                check_type(argname="argument acm_pca_arn", value=acm_pca_arn, expected_type=type_hints["acm_pca_arn"])
                check_type(argname="argument x509_certificate_data", value=x509_certificate_data, expected_type=type_hints["x509_certificate_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acm_pca_arn is not None:
                self._values["acm_pca_arn"] = acm_pca_arn
            if x509_certificate_data is not None:
                self._values["x509_certificate_data"] = x509_certificate_data

        @builtins.property
        def acm_pca_arn(self) -> typing.Optional[builtins.str]:
            '''The root certificate of the AWS Private Certificate Authority specified by this ARN is used in trust validation for temporary credential requests.

            Included for trust anchors of type ``AWS_ACM_PCA`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-sourcedata.html#cfn-rolesanywhere-trustanchor-sourcedata-acmpcaarn
            '''
            result = self._values.get("acm_pca_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def x509_certificate_data(self) -> typing.Optional[builtins.str]:
            '''The PEM-encoded data for the certificate anchor.

            Included for trust anchors of type ``CERTIFICATE_BUNDLE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-sourcedata.html#cfn-rolesanywhere-trustanchor-sourcedata-x509certificatedata
            '''
            result = self._values.get("x509_certificate_data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-rolesanywhere.CfnTrustAnchor.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={"source_data": "sourceData", "source_type": "sourceType"},
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            source_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTrustAnchor.SourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Object representing the TrustAnchor type and its related certificate data.

            :param source_data: A union object representing the data field of the TrustAnchor depending on its type.
            :param source_type: The type of the TrustAnchor.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_rolesanywhere as rolesanywhere
                
                source_property = rolesanywhere.CfnTrustAnchor.SourceProperty(
                    source_data=rolesanywhere.CfnTrustAnchor.SourceDataProperty(
                        acm_pca_arn="acmPcaArn",
                        x509_certificate_data="x509CertificateData"
                    ),
                    source_type="sourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b610749321e5d894fa43eb572b75e064a593cd1b2e04fb219356bf8d7701ed84)
                check_type(argname="argument source_data", value=source_data, expected_type=type_hints["source_data"])
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_data is not None:
                self._values["source_data"] = source_data
            if source_type is not None:
                self._values["source_type"] = source_type

        @builtins.property
        def source_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTrustAnchor.SourceDataProperty"]]:
            '''A union object representing the data field of the TrustAnchor depending on its type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-source.html#cfn-rolesanywhere-trustanchor-source-sourcedata
            '''
            result = self._values.get("source_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTrustAnchor.SourceDataProperty"]], result)

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''The type of the TrustAnchor.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-source.html#cfn-rolesanywhere-trustanchor-source-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-rolesanywhere.CfnTrustAnchorProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "name": "name",
        "source": "source",
        "tags": "tags",
    },
)
class CfnTrustAnchorProps:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTrustAnchor.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTrustAnchor``.

        :param enabled: Indicates whether the trust anchor is enabled.
        :param name: The name of the trust anchor.
        :param source: The trust anchor type and its related certificate data.
        :param tags: A list of tags to attach to the trust anchor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_rolesanywhere as rolesanywhere
            
            cfn_trust_anchor_props = rolesanywhere.CfnTrustAnchorProps(
                enabled=False,
                name="name",
                source=rolesanywhere.CfnTrustAnchor.SourceProperty(
                    source_data=rolesanywhere.CfnTrustAnchor.SourceDataProperty(
                        acm_pca_arn="acmPcaArn",
                        x509_certificate_data="x509CertificateData"
                    ),
                    source_type="sourceType"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ae5f2e117f4c30b8fa4ad9bb22ad2e5a1985464f7ac9ab673663ae2dd70699)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if name is not None:
            self._values["name"] = name
        if source is not None:
            self._values["source"] = source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether the trust anchor is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the trust anchor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTrustAnchor.SourceProperty]]:
        '''The trust anchor type and its related certificate data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTrustAnchor.SourceProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of tags to attach to the trust anchor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrustAnchorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCRL",
    "CfnCRLProps",
    "CfnProfile",
    "CfnProfileProps",
    "CfnTrustAnchor",
    "CfnTrustAnchorProps",
]

publication.publish()

def _typecheckingstub__a1f5127a6072e3e1594ed84e52ee329f0bec784663210b882365111bcb9d74c1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    crl_data: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust_anchor_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57745232024b81a7bb1d3b6309e92eb2b57e18d190b4f7b79d5efe0fbcd20c9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1453dbfe2782a40ac1a42e90244804217bcefdbb157c124d04a2fba86404c021(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac2a0417b0966cae3171dc1f30922ee70d6d033d75a5944fa3c161bf241815f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5dd36764c4929bb8117db2f2886f48bef59cff15515ca943449ba13a386a4d2(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f232a9f7129ce024864783b6e54b238dce6eec305747da4ed6e4dddacf1ccd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a54775207bd13031efb15e0a837a922056023b06fc4872cb6d2fe831f3348e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7213a68a2891838e5c133b3c0895cdabe1415dbe03f8c3ef8cae71574d42357e(
    *,
    crl_data: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust_anchor_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6806ee15cca56bda4267a22b759ed8375cd2e62db06437e7f09fada55005a7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    duration_seconds: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    require_instance_properties: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce153bf3134dbba710a985eb2442ada7df6017ca5f6bd0dd8f53e470425671a4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc02f0e47776966423a52563a72de0d29aab0ad8adb1e7355ed108924b9d233(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074dbf3efe952e42283ffde79193facf80b79723a75d5014cd3b6415dcbc7aa2(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8af40145f48856b43419fd448c6d8600ca768f15d59172027f57763f6a48c98(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aefe2ad624ae5cf970333bbdfaf8c18ede4b858175bddef4bdf378de4e662b2(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f247d3c51644191eaec666b0a9d9a314cec1a8429887d9d0a6e6b7a40269408(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa27d61e7c7f776e6f4a2967444d750b22d35d07301e48387a3982103c698e54(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44b61b11fdd9225ee855d6e3e295ff98a14b4378d514b0483bd7a83fa7fbad0(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186c9185f0e3d382d003898d6e137d4486b32d8fbf5677e0314503cf4d058485(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68479953be44aa9e517847e17515e2e417b0906a41d1593d6e862765cc542971(
    *,
    duration_seconds: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    require_instance_properties: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6896e80f72d00d000494119ad365fe5d1d1b7020e2013f9e9b0d6323a75c949(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTrustAnchor.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8c29dd3eac7196a5ce9f905ba42b5ffe6b2951973715c23176171e7438c6ec(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267ce50452d28a82d4fbbe6ecfdf6d51ccc17a2c41a247c219be70700b8abca3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfc52bdcd353242b1cc3874b0ad92fd3241bc0a94166599dacfb27c12384623(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7737804f567c8e53cbf1fe4bdfda25aa66fa2e485937face7b9ff01d2010245(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bed2153cb8af0544f782db5b3fe21582f9500bcb5f1c2f3ce9cb7721cba9455(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTrustAnchor.SourceProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047566853c0f637ae8d56c48d17fcede72c704aa1cd6f955dbd6669d480e4be2(
    *,
    acm_pca_arn: typing.Optional[builtins.str] = None,
    x509_certificate_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b610749321e5d894fa43eb572b75e064a593cd1b2e04fb219356bf8d7701ed84(
    *,
    source_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTrustAnchor.SourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ae5f2e117f4c30b8fa4ad9bb22ad2e5a1985464f7ac9ab673663ae2dd70699(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTrustAnchor.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
