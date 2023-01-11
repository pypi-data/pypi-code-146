'''
# AWS::RolesAnywhere Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as rolesanywhere
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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnCRL(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_rolesanywhere.CfnCRL",
):
    '''A CloudFormation ``AWS::RolesAnywhere::CRL``.

    Creates a Crl.

    :cloudformationResource: AWS::RolesAnywhere::CRL
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_rolesanywhere as rolesanywhere
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        crl_data: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__faad4fb44ea6962d83fbccf0b877358e66cd23bb56005c143a26a2684c761841)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c926547f0f71fca2a589c8aa74e1928a85798167e3971815a4d39a4f9708c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6228358dd9f132fcbc711af79e8c7a96e258139a69a99853078aff48e587a587)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7c01489711403d4bb47434c5e282944f424f52fc8c825c4fed943fe190d1eeaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crlData", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''The enabled status of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612f01a4c40143f30e4a4c7d5171277b37f63f9319f43de62a5f9cb8a4bca467)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92c256fa916282c5d3ec3dcebe4efdc49e406bb853be0693d54f3b78cd4d4b76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e85d04da0d98c352d24a991d45adfbcfcf6cc5fd942ebf799a7732f6d1a879b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustAnchorArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_rolesanywhere.CfnCRLProps",
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
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_rolesanywhere as rolesanywhere
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a1f77a3ab5b93afacc04b5918d100de85dd7f92cf504f8d4c2c491e5ed42205)
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
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''The enabled status of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The customer specified name of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

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


@jsii.implements(_IInspectable_82c04a63)
class CfnProfile(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_rolesanywhere.CfnProfile",
):
    '''A CloudFormation ``AWS::RolesAnywhere::Profile``.

    Creates a Profile.

    :cloudformationResource: AWS::RolesAnywhere::Profile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_rolesanywhere as rolesanywhere
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        duration_seconds: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        require_instance_properties: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb7aeefe168dbe6686ed37bfe3ebadcaaa9aafbb4ae6022147e34ffb68acbc24)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368952096e1a72b72c2f1b2b95b545f27f1584d7220de793962be0adcf04490a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69a6190bd5eb3222d96a3065c19e52e675cc17513a12d09ec25bd69b7febe76b)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b9a630741b8a2c1ee009524ef5b7ccd52f072c2ef222b1187900878b35375bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''The enabled status of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f4663a76f9f56040882b99a8ab43a8d87d363717f8e7e529ac693317e6f9d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__113b33904d9f70489efd3e8572bb6f40daa4703ebf409beb16b1fd8945b52add)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bb8d371340480c16f652ecef65a24e791db9f90809b152a45df6b849c97197f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="requireInstanceProperties")
    def require_instance_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether instance properties are required in CreateSession requests with this profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-requireinstanceproperties
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "requireInstanceProperties"))

    @require_instance_properties.setter
    def require_instance_properties(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6925a01faa02715f8413c443217c63e66c830296b91aab828009f30f6ee47c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7203d0d76608caaf60a21e959f1028e69cd709fb377cd1850263862413984ea2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d54b022ce0b141d16070eda33551ee09f30023ba972dce84ccb7dc38fb59ae85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionPolicy", value)


@jsii.data_type(
    jsii_type="monocdk.aws_rolesanywhere.CfnProfileProps",
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
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        require_instance_properties: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_rolesanywhere as rolesanywhere
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b6fa424b33d6985d63b590009886480f854ddc846565c6b0ce6074475f96108)
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
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''The enabled status of the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

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
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether instance properties are required in CreateSession requests with this profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-requireinstanceproperties
        '''
        result = self._values.get("require_instance_properties")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of Tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTrustAnchor(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_rolesanywhere.CfnTrustAnchor",
):
    '''A CloudFormation ``AWS::RolesAnywhere::TrustAnchor``.

    Creates a TrustAnchor.

    :cloudformationResource: AWS::RolesAnywhere::TrustAnchor
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_rolesanywhere as rolesanywhere
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union[typing.Union["CfnTrustAnchor.SourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__28c151a9dd18c336726c9cbeeae532ab81b8a4c74e95998920100b4a19e11450)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTrustAnchorProps(
            enabled=enabled, name=name, source=source, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b166cd89a972672af4c21bfd6eb6191dedd0f1e1d37aa4473e1c5b0c2a35d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8897ca41500d341b17c502053221aa44fd4d8cdc7a244bbabce63cc949ebbf1)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags to attach to the trust anchor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether the trust anchor is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e471a3c8b61a61f7ec930456254705f7c79f5bdd8ad7dedbf96ea1b0874915)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c99e9c7230c307a7724db30d142562c07682c7f459e12edb6154ee722a1b967f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(
        self,
    ) -> typing.Optional[typing.Union["CfnTrustAnchor.SourceProperty", _IResolvable_a771d0ef]]:
        '''The trust anchor type and its related certificate data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-source
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTrustAnchor.SourceProperty", _IResolvable_a771d0ef]], jsii.get(self, "source"))

    @source.setter
    def source(
        self,
        value: typing.Optional[typing.Union["CfnTrustAnchor.SourceProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfc839f1c46de748ac3009d6c48e5ec0a992a9e712bdf58470ec4f52a05f6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_rolesanywhere.CfnTrustAnchor.SourceDataProperty",
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
                from monocdk import aws_rolesanywhere as rolesanywhere
                
                source_data_property = rolesanywhere.CfnTrustAnchor.SourceDataProperty(
                    acm_pca_arn="acmPcaArn",
                    x509_certificate_data="x509CertificateData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d243d471ef887954984d8119518bf077ed83b4c0115aa582152cfd83076c065)
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
        jsii_type="monocdk.aws_rolesanywhere.CfnTrustAnchor.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={"source_data": "sourceData", "source_type": "sourceType"},
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            source_data: typing.Optional[typing.Union[typing.Union["CfnTrustAnchor.SourceDataProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_rolesanywhere as rolesanywhere
                
                source_property = rolesanywhere.CfnTrustAnchor.SourceProperty(
                    source_data=rolesanywhere.CfnTrustAnchor.SourceDataProperty(
                        acm_pca_arn="acmPcaArn",
                        x509_certificate_data="x509CertificateData"
                    ),
                    source_type="sourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00e870c31809f874f8fe6eabe3a2f25e05d262bd8b2309e26b41ed698d35322a)
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
        ) -> typing.Optional[typing.Union["CfnTrustAnchor.SourceDataProperty", _IResolvable_a771d0ef]]:
            '''A union object representing the data field of the TrustAnchor depending on its type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-source.html#cfn-rolesanywhere-trustanchor-source-sourcedata
            '''
            result = self._values.get("source_data")
            return typing.cast(typing.Optional[typing.Union["CfnTrustAnchor.SourceDataProperty", _IResolvable_a771d0ef]], result)

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
    jsii_type="monocdk.aws_rolesanywhere.CfnTrustAnchorProps",
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
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union[typing.Union[CfnTrustAnchor.SourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_rolesanywhere as rolesanywhere
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9e2874ef4de9ac1292d2cdbb37bebb68cd8f542ccb2ed5de5aaa3347bed8356)
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
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether the trust anchor is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

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
    ) -> typing.Optional[typing.Union[CfnTrustAnchor.SourceProperty, _IResolvable_a771d0ef]]:
        '''The trust anchor type and its related certificate data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[CfnTrustAnchor.SourceProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags to attach to the trust anchor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

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

def _typecheckingstub__faad4fb44ea6962d83fbccf0b877358e66cd23bb56005c143a26a2684c761841(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    crl_data: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust_anchor_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c926547f0f71fca2a589c8aa74e1928a85798167e3971815a4d39a4f9708c4(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6228358dd9f132fcbc711af79e8c7a96e258139a69a99853078aff48e587a587(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c01489711403d4bb47434c5e282944f424f52fc8c825c4fed943fe190d1eeaa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612f01a4c40143f30e4a4c7d5171277b37f63f9319f43de62a5f9cb8a4bca467(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c256fa916282c5d3ec3dcebe4efdc49e406bb853be0693d54f3b78cd4d4b76(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e85d04da0d98c352d24a991d45adfbcfcf6cc5fd942ebf799a7732f6d1a879b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1f77a3ab5b93afacc04b5918d100de85dd7f92cf504f8d4c2c491e5ed42205(
    *,
    crl_data: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust_anchor_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7aeefe168dbe6686ed37bfe3ebadcaaa9aafbb4ae6022147e34ffb68acbc24(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    duration_seconds: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    require_instance_properties: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368952096e1a72b72c2f1b2b95b545f27f1584d7220de793962be0adcf04490a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a6190bd5eb3222d96a3065c19e52e675cc17513a12d09ec25bd69b7febe76b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a630741b8a2c1ee009524ef5b7ccd52f072c2ef222b1187900878b35375bd0(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f4663a76f9f56040882b99a8ab43a8d87d363717f8e7e529ac693317e6f9d7(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113b33904d9f70489efd3e8572bb6f40daa4703ebf409beb16b1fd8945b52add(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb8d371340480c16f652ecef65a24e791db9f90809b152a45df6b849c97197f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6925a01faa02715f8413c443217c63e66c830296b91aab828009f30f6ee47c8(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7203d0d76608caaf60a21e959f1028e69cd709fb377cd1850263862413984ea2(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54b022ce0b141d16070eda33551ee09f30023ba972dce84ccb7dc38fb59ae85(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6fa424b33d6985d63b590009886480f854ddc846565c6b0ce6074475f96108(
    *,
    duration_seconds: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    require_instance_properties: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c151a9dd18c336726c9cbeeae532ab81b8a4c74e95998920100b4a19e11450(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[typing.Union[CfnTrustAnchor.SourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b166cd89a972672af4c21bfd6eb6191dedd0f1e1d37aa4473e1c5b0c2a35d6(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8897ca41500d341b17c502053221aa44fd4d8cdc7a244bbabce63cc949ebbf1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e471a3c8b61a61f7ec930456254705f7c79f5bdd8ad7dedbf96ea1b0874915(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99e9c7230c307a7724db30d142562c07682c7f459e12edb6154ee722a1b967f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfc839f1c46de748ac3009d6c48e5ec0a992a9e712bdf58470ec4f52a05f6ed(
    value: typing.Optional[typing.Union[CfnTrustAnchor.SourceProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d243d471ef887954984d8119518bf077ed83b4c0115aa582152cfd83076c065(
    *,
    acm_pca_arn: typing.Optional[builtins.str] = None,
    x509_certificate_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e870c31809f874f8fe6eabe3a2f25e05d262bd8b2309e26b41ed698d35322a(
    *,
    source_data: typing.Optional[typing.Union[typing.Union[CfnTrustAnchor.SourceDataProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e2874ef4de9ac1292d2cdbb37bebb68cd8f542ccb2ed5de5aaa3347bed8356(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[typing.Union[CfnTrustAnchor.SourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
