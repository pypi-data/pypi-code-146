'''
# AWS::VoiceID Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as voiceid
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for VoiceID construct libraries](https://constructs.dev/search?q=voiceid)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::VoiceID resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VoiceID.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::VoiceID](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VoiceID.html).

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
class CfnDomain(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_voiceid.CfnDomain",
):
    '''A CloudFormation ``AWS::VoiceID::Domain``.

    Creates a domain that contains all Amazon Connect Voice ID data, such as speakers, fraudsters, customer audio, and voiceprints.

    :cloudformationResource: AWS::VoiceID::Domain
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_voiceid as voiceid
        
        cfn_domain = voiceid.CfnDomain(self, "MyCfnDomain",
            name="name",
            server_side_encryption_configuration=voiceid.CfnDomain.ServerSideEncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
            ),
        
            # the properties below are optional
            description="description",
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
        name: builtins.str,
        server_side_encryption_configuration: typing.Union[typing.Union["CfnDomain.ServerSideEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VoiceID::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The client-provided name for the domain.
        :param server_side_encryption_configuration: The server-side encryption configuration containing the KMS key identifier you want Voice ID to use to encrypt your data.
        :param description: The client-provided description of the domain.
        :param tags: The tags used to organize, track, or control access for this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e03aa2f143aaefcb4f1e888bd9c4f23369ce4fa8b8c3d8be4fb3ef56bdaab6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainProps(
            name=name,
            server_side_encryption_configuration=server_side_encryption_configuration,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2981648d24c5efa7fa43c75978ccfd929b1d237152c49edb7a65e6e57fe29247)
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
            type_hints = typing.get_type_hints(_typecheckingstub__081fef531aedf595dbdef21db87b942b3dc10ef878fe36451b238fdcaa3e9b2e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainId")
    def attr_domain_id(self) -> builtins.str:
        '''The identifier of the domain.

        :cloudformationAttribute: DomainId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html#cfn-voiceid-domain-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The client-provided name for the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html#cfn-voiceid-domain-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6c779e7c5080dea076e1e0208bd0e560a36ff3a43b4575fb5f5cafa9c7d925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> typing.Union["CfnDomain.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]:
        '''The server-side encryption configuration containing the KMS key identifier you want Voice ID to use to encrypt your data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html#cfn-voiceid-domain-serversideencryptionconfiguration
        '''
        return typing.cast(typing.Union["CfnDomain.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "serverSideEncryptionConfiguration"))

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(
        self,
        value: typing.Union["CfnDomain.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3babe95bb9c86ab1583c538e31ccc7f509204e20f4b3937090d29603cd1fca32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideEncryptionConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The client-provided description of the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html#cfn-voiceid-domain-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe8be8a8e35f4a3af732ea377b1b941a65818cb5c0c1e441fe752c8226c06c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_voiceid.CfnDomain.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: builtins.str) -> None:
            '''The configuration containing information about the customer managed key used for encrypting customer data.

            :param kms_key_id: The identifier of the KMS key to use to encrypt data stored by Voice ID. Voice ID doesn't support asymmetric customer managed keys .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-voiceid-domain-serversideencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_voiceid as voiceid
                
                server_side_encryption_configuration_property = voiceid.CfnDomain.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59fb3a4b7749de94274e184f749531bea01a9800c05516642cdaa5095a639261)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "kms_key_id": kms_key_id,
            }

        @builtins.property
        def kms_key_id(self) -> builtins.str:
            '''The identifier of the KMS key to use to encrypt data stored by Voice ID.

            Voice ID doesn't support asymmetric customer managed keys .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-voiceid-domain-serversideencryptionconfiguration.html#cfn-voiceid-domain-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            assert result is not None, "Required property 'kms_key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_voiceid.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "description": "description",
        "tags": "tags",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        server_side_encryption_configuration: typing.Union[typing.Union[CfnDomain.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDomain``.

        :param name: The client-provided name for the domain.
        :param server_side_encryption_configuration: The server-side encryption configuration containing the KMS key identifier you want Voice ID to use to encrypt your data.
        :param description: The client-provided description of the domain.
        :param tags: The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_voiceid as voiceid
            
            cfn_domain_props = voiceid.CfnDomainProps(
                name="name",
                server_side_encryption_configuration=voiceid.CfnDomain.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ffa7285040abdb3a2feef8c6c46c6d9022e9720afd4ff2e5d5783f42ec8d72)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "server_side_encryption_configuration": server_side_encryption_configuration,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The client-provided name for the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html#cfn-voiceid-domain-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Union[CfnDomain.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef]:
        '''The server-side encryption configuration containing the KMS key identifier you want Voice ID to use to encrypt your data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html#cfn-voiceid-domain-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        assert result is not None, "Required property 'server_side_encryption_configuration' is missing"
        return typing.cast(typing.Union[CfnDomain.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The client-provided description of the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html#cfn-voiceid-domain-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-voiceid-domain.html#cfn-voiceid-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDomain",
    "CfnDomainProps",
]

publication.publish()

def _typecheckingstub__71e03aa2f143aaefcb4f1e888bd9c4f23369ce4fa8b8c3d8be4fb3ef56bdaab6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    server_side_encryption_configuration: typing.Union[typing.Union[CfnDomain.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2981648d24c5efa7fa43c75978ccfd929b1d237152c49edb7a65e6e57fe29247(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081fef531aedf595dbdef21db87b942b3dc10ef878fe36451b238fdcaa3e9b2e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6c779e7c5080dea076e1e0208bd0e560a36ff3a43b4575fb5f5cafa9c7d925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3babe95bb9c86ab1583c538e31ccc7f509204e20f4b3937090d29603cd1fca32(
    value: typing.Union[CfnDomain.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe8be8a8e35f4a3af732ea377b1b941a65818cb5c0c1e441fe752c8226c06c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fb3a4b7749de94274e184f749531bea01a9800c05516642cdaa5095a639261(
    *,
    kms_key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ffa7285040abdb3a2feef8c6c46c6d9022e9720afd4ff2e5d5783f42ec8d72(
    *,
    name: builtins.str,
    server_side_encryption_configuration: typing.Union[typing.Union[CfnDomain.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
