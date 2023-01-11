'''
# Amazon Pinpoint Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_pinpoint as pinpoint
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Pinpoint construct libraries](https://constructs.dev/search?q=pinpoint)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Pinpoint resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Pinpoint.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Pinpoint](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Pinpoint.html).

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
class CfnADMChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnADMChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::ADMChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the ADM channel to send push notifications through the Amazon Device Messaging (ADM) service to apps that run on Amazon devices, such as Kindle Fire tablets. Before you can use Amazon Pinpoint to send messages to Amazon devices, you have to enable the ADM channel for an Amazon Pinpoint application.

    The ADMChannel resource represents the status and authentication settings for the ADM channel for an application.

    :cloudformationResource: AWS::Pinpoint::ADMChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_aDMChannel = pinpoint.CfnADMChannel(self, "MyCfnADMChannel",
            application_id="applicationId",
            client_id="clientId",
            client_secret="clientSecret",
        
            # the properties below are optional
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::ADMChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.
        :param client_id: The Client ID that you received from Amazon to send messages by using ADM.
        :param client_secret: The Client Secret that you received from Amazon to send messages by using ADM.
        :param enabled: Specifies whether to enable the ADM channel for the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89edf7657f2dc9f670d88e0dec8cfcdc9581aa90914d2fbc0740cc5b0b3684c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnADMChannelProps(
            application_id=application_id,
            client_id=client_id,
            client_secret=client_secret,
            enabled=enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ff400797b6af54e2f2d3c814d120e8481cc789961dbd74cf0247eb76a8aa42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__083070488dc8a3a1931e8c3c551a3eda6b3d1dd55c4a0f5503e92fbb25c0f8c2)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c7d63916548b2a6b7e6e97faba0331d844d3371e9665c0ce8112a4ff5e8ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        '''The Client ID that you received from Amazon to send messages by using ADM.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientid
        '''
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea31fb98f19d82b67b3ead2a86c75157d3c035e8955e97b62d438df00382ab89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        '''The Client Secret that you received from Amazon to send messages by using ADM.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientsecret
        '''
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808f1624697403c9bfbde0547b92a6655474619708864d71409ffa5fed93bc5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the ADM channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8c7f61c0f0495f977773a1a5558cbcdf5462444a65e68f085a2f1ce5e10a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnADMChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "enabled": "enabled",
    },
)
class CfnADMChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnADMChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.
        :param client_id: The Client ID that you received from Amazon to send messages by using ADM.
        :param client_secret: The Client Secret that you received from Amazon to send messages by using ADM.
        :param enabled: Specifies whether to enable the ADM channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_aDMChannel_props = pinpoint.CfnADMChannelProps(
                application_id="applicationId",
                client_id="clientId",
                client_secret="clientSecret",
            
                # the properties below are optional
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd63651bdc32d38170be7c4a4ea62566f564977bb03c5be3bc885bbd0cb4b2ad)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The Client ID that you received from Amazon to send messages by using ADM.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientid
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''The Client Secret that you received from Amazon to send messages by using ADM.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientsecret
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the ADM channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnADMChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAPNSChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnAPNSChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::APNSChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the APNs channel to send push notification messages to the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send notifications to APNs, you have to enable the APNs channel for an Amazon Pinpoint application.

    The APNSChannel resource represents the status and authentication settings for the APNs channel for an application.

    :cloudformationResource: AWS::Pinpoint::APNSChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_aPNSChannel = pinpoint.CfnAPNSChannel(self, "MyCfnAPNSChannel",
            application_id="applicationId",
        
            # the properties below are optional
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::APNSChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs channel for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9feda3513378ee7fef3c8c73037158787d185952d582ff1d512313660b5dbf0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAPNSChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549a6e427ed22bf2722c1530341ccb5c8731351051e45613d62a97512e5353c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fbf18ec330cbafb33e965633cf7f20d2989b90762d2689e87d80313dd2d3cf5)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31abf31a748027b68f1c4a64decf362d8e81293755e50cab38fcafb60b78d5f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-bundleid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33058b558e8b0e12e81768ce69e2884234f2eeb4127087c9187e30abf36832ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ef6ff9c72c4b1b3764a80c5d829db3642e11c6fd5aa35ed51e904d898ca026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-defaultauthenticationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAuthenticationMethod"))

    @default_authentication_method.setter
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09937094f310fa7f154a19107081618c010e7c0a0315778a8429bd4213c074da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the APNs channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4a195981c1f67de79a8a3e8ea152a7fa2337d3cc1f42fca84002df3de0381d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099692d77a41da495fb6ea6c75c2f338b3bf6aea24719f52c296c0614ded53ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-teamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d191bea5990946338f62313d34a933cd099da0a14b35c1711698f58576a8c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKey"))

    @token_key.setter
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c508dfee6a703b62c905e6c6f3cdf517ff0f2b1c10eef24ba9d037ea4f4edb37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKey", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKeyId"))

    @token_key_id.setter
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa16b10aeccbaec0fbfc0c09826479294f7844fadaef7478f11734d1d856a54c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnAPNSChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAPNSChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs channel for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_aPNSChannel_props = pinpoint.CfnAPNSChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df1012692ddb95edd94a29e46e3c37bde870b6b39cf2ed492aeca9a98c9174e)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the APNs channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAPNSSandboxChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnAPNSSandboxChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::APNSSandboxChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the APNs sandbox channel to send push notification messages to the sandbox environment of the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send notifications to the APNs sandbox environment, you have to enable the APNs sandbox channel for an Amazon Pinpoint application.

    The APNSSandboxChannel resource represents the status and authentication settings of the APNs sandbox channel for an application.

    :cloudformationResource: AWS::Pinpoint::APNSSandboxChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_aPNSSandbox_channel = pinpoint.CfnAPNSSandboxChannel(self, "MyCfnAPNSSandboxChannel",
            application_id="applicationId",
        
            # the properties below are optional
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::APNSSandboxChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df97cce65ed8aaf553b9054297eb52594bf98f44af0b32fa02822147c8f4ca4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAPNSSandboxChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc43c02fb32e7af990c8eb8e2d163c1bea0a3ec6ccd3fde5678b68604ed09e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0218f15734a3890a35ed3acdff40abc74e04d7a45fd18a9d85dadd7b19b8f219)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6206f551682501c583efaa443f65098ac5afefd1cfc7de199e2e2993424c714a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-bundleid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd9767f7fc70860d849070a5b642b96885183f62eeef538b2d9dfa83347a0ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b96de92128eecce5d4a3d24f1b3dca6381dfddb6971061a10a78e85e4158805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-defaultauthenticationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAuthenticationMethod"))

    @default_authentication_method.setter
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4dcbeb2f35cb493fdec1205723efabab5a2b709eb31237c502ac5d5618b0f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3081fe81131829bb7ee65429e89ffa73c0ded99af807b98d1535543d19e397b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85c9977ecd52bbd3954500b80fcfea9b850085e111b606b190ba46cf9562180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-teamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865d16a41042cf472e4157a0175c083a52433b4013f88ca69de890d5eaee17bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKey"))

    @token_key.setter
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52663a851c27d4ccdd4b2c4ded455f019567b5807157a41c57b009de8be9f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKey", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKeyId"))

    @token_key_id.setter
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dadb03b9f90459ed52ee988277fe121bb2dff301a0f6cea8a1a9b6dbeed37d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnAPNSSandboxChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSSandboxChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAPNSSandboxChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_aPNSSandbox_channel_props = pinpoint.CfnAPNSSandboxChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411b5bef1c3d579e00dd53ac839ad5a1c6a3b157fd563191814177fab9c24f77)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSSandboxChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAPNSVoipChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnAPNSVoipChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::APNSVoipChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the APNs VoIP channel to send VoIP notification messages to the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send VoIP notifications to APNs, you have to enable the APNs VoIP channel for an Amazon Pinpoint application.

    The APNSVoipChannel resource represents the status and authentication settings of the APNs VoIP channel for an application.

    :cloudformationResource: AWS::Pinpoint::APNSVoipChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_aPNSVoip_channel = pinpoint.CfnAPNSVoipChannel(self, "MyCfnAPNSVoipChannel",
            application_id="applicationId",
        
            # the properties below are optional
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::APNSVoipChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23406e640ee8559d65d605cf6019e589ca1f122cd388387a80adc1925eb73769)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAPNSVoipChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6676c9280805c25076072ae0326cffa05dd8471a01e4dd4be0711466a3d58eeb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__880fc2f7e4f8b2a9f24e91dd282350faadbaa03dd37ccc77ca647eb101c6eba5)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92dac5bbc68e29ed312064e45d44376582fbeb28bd83d7af1d2ab210309ddb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-bundleid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72df9ddff41ffbcc6c8c89aabb0077ae2ea9a90657d4b65a0eff889c0783858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9c46429af8a3a4f4bca70143a869245dab91385cffa27794b3a1d178269b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-defaultauthenticationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAuthenticationMethod"))

    @default_authentication_method.setter
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1559b15b2148192307edd48d114f38aefefd9e53082b84d6ea4312552afe4d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e1e94ef8d29e3ab5cde7c8f72d06b8290d334d526d87f6d2fdf2c006d875ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d29f21761a33e992d22f076f1bb6a0acc87140fc506ccef8bd5f187354f351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-teamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d349da5eebb40c1d34d92c7ab3611b362c2234ff4d8c29af1c17d2893611f24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKey"))

    @token_key.setter
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ee4183b1669eab7d1171c938c4685f2c53512f43e03a448716f966aa21b76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKey", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKeyId"))

    @token_key_id.setter
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41098345792d576241caac84f1711e120d64963b3e30f223926621003522a77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnAPNSVoipChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSVoipChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAPNSVoipChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_aPNSVoip_channel_props = pinpoint.CfnAPNSVoipChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f2664afa90492fb1bbb2a91abd1a44b2e09a85874925d509d55be50ff67a0f)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSVoipChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAPNSVoipSandboxChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnAPNSVoipSandboxChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::APNSVoipSandboxChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the APNs VoIP sandbox channel to send VoIP notification messages to the sandbox environment of the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send VoIP notifications to the APNs sandbox environment, you have to enable the APNs VoIP sandbox channel for an Amazon Pinpoint application.

    The APNSVoipSandboxChannel resource represents the status and authentication settings of the APNs VoIP sandbox channel for an application.

    :cloudformationResource: AWS::Pinpoint::APNSVoipSandboxChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_aPNSVoip_sandbox_channel = pinpoint.CfnAPNSVoipSandboxChannel(self, "MyCfnAPNSVoipSandboxChannel",
            application_id="applicationId",
        
            # the properties below are optional
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::APNSVoipSandboxChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the application that the APNs VoIP sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether the APNs VoIP sandbox channel is enabled for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.
        :param team_id: The identifier that's assigned to your Apple developer account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb121d47466f6ab933fdba78a10babeee30fe2e5d4f9385be72b0968cff8fc8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAPNSVoipSandboxChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c66e56ccb64009018dc4f00616d2d80b181ff814f6c41919eee8a383e4be4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__115c73adc974eeaa28e0097b9852b287746c56bf189263dfb1222395c3680851)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the application that the APNs VoIP sandbox channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c372c52dee15e202b12adc6834e5e4c1acf718a0b729fb2fb0235ce20a17c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-bundleid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed65bf4387c96499a3d56399003709f17bb281c0a37d48d72b7034402f6e039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f826be23fe72cd9df2e36b34c119783db08e0f83e699d2c0443e5bfff724a573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-defaultauthenticationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAuthenticationMethod"))

    @default_authentication_method.setter
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468af95861da2dfcfcdc705468190cdd8f6c12163f8461c1f98ec218f8224e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the APNs VoIP sandbox channel is enabled for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2355b430e7729e890a58439a96ed13ccedfe88064ff7160c89b1fe4be5cc49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2498da1460d4b163a22fb98a4810c9e6ad3a0cb9e58e0f7d83059a7bc89d7566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple developer account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-teamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8822b3b59b5cd7ee3ce26d710ce38acf1f442d0a46a3c5383e1230bf990352d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKey"))

    @token_key.setter
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e5f1eeed61d8c7aff29f9f5189c94269b7900569f4a87f198c94c1bd1bb20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKey", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKeyId"))

    @token_key_id.setter
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436070a4aeed9b794640b0ee686010965402379283f2e4e922ed8bf6b1fb8fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnAPNSVoipSandboxChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSVoipSandboxChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAPNSVoipSandboxChannel``.

        :param application_id: The unique identifier for the application that the APNs VoIP sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether the APNs VoIP sandbox channel is enabled for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.
        :param team_id: The identifier that's assigned to your Apple developer account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_aPNSVoip_sandbox_channel_props = pinpoint.CfnAPNSVoipSandboxChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b99e4cd78c895269dbe48d9f84ff34d894b35642cc012e927d3d770bcf66ee)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the application that the APNs VoIP sandbox channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the APNs VoIP sandbox channel is enabled for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple developer account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSVoipSandboxChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApp(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnApp",
):
    '''A CloudFormation ``AWS::Pinpoint::App``.

    An *app* is an Amazon Pinpoint application, also referred to as a *project* . An application is a collection of related settings, customer information, segments, campaigns, and other types of Amazon Pinpoint resources.

    The App resource represents an Amazon Pinpoint application.

    :cloudformationResource: AWS::Pinpoint::App
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        # tags: Any
        
        cfn_app = pinpoint.CfnApp(self, "MyCfnApp",
            name="name",
        
            # the properties below are optional
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The display name of the application.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498e015913faa51042166627026ab7531855376d5c70623d211ce1ec8a74dc7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppProps(name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ed1a25988742ce022a803761f9650e64e228bde96f12e192ff6584692d05b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd8483cf96c83ad5d24abd9ce0ee83fe485d71f6973a042b0d79a7b5b824c1b8)
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
        '''The Amazon Resource Name (ARN) of the application.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The display name of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd57e24f1f8059648325e2e6c6ce87380ca1795f817ad928cead51fb90be5f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnAppProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnAppProps:
    def __init__(self, *, name: builtins.str, tags: typing.Any = None) -> None:
        '''Properties for defining a ``CfnApp``.

        :param name: The display name of the application.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            # tags: Any
            
            cfn_app_props = pinpoint.CfnAppProps(
                name="name",
            
                # the properties below are optional
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a33a4ae44d4e8f6fa7a80007fffc14e3a26d5b9ab8024c3142107b792f1ddc8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The display name of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplicationSettings(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnApplicationSettings",
):
    '''A CloudFormation ``AWS::Pinpoint::ApplicationSettings``.

    Specifies the settings for an Amazon Pinpoint application. In Amazon Pinpoint, an *application* (also referred to as an *app* or *project* ) is a collection of related settings, customer information, segments, and campaigns, and other types of Amazon Pinpoint resources.

    :cloudformationResource: AWS::Pinpoint::ApplicationSettings
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_application_settings = pinpoint.CfnApplicationSettings(self, "MyCfnApplicationSettings",
            application_id="applicationId",
        
            # the properties below are optional
            campaign_hook=pinpoint.CfnApplicationSettings.CampaignHookProperty(
                lambda_function_name="lambdaFunctionName",
                mode="mode",
                web_url="webUrl"
            ),
            cloud_watch_metrics_enabled=False,
            limits=pinpoint.CfnApplicationSettings.LimitsProperty(
                daily=123,
                maximum_duration=123,
                messages_per_second=123,
                total=123
            ),
            quiet_time=pinpoint.CfnApplicationSettings.QuietTimeProperty(
                end="end",
                start="start"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        campaign_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplicationSettings.CampaignHookProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        limits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplicationSettings.LimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        quiet_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplicationSettings.QuietTimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::ApplicationSettings``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application.
        :param campaign_hook: The settings for the Lambda function to use by default as a code hook for campaigns in the application. To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.
        :param cloud_watch_metrics_enabled: Specifies whether to enable application-related alarms in Amazon CloudWatch.
        :param limits: The default sending limits for campaigns in the application. To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.
        :param quiet_time: The default quiet time for campaigns in the application. Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met: - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value. - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings). - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings). If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled. To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4a69f1b475b10bba93b972e6b823e3e22ebf7d1a3d5d35427ed7dbc12ff6e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationSettingsProps(
            application_id=application_id,
            campaign_hook=campaign_hook,
            cloud_watch_metrics_enabled=cloud_watch_metrics_enabled,
            limits=limits,
            quiet_time=quiet_time,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4e7900110fae058427efccfbfa284f4572d4988df7a17be671d86debe0c866)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2a9bf62737da228011aabc0ffd0ae507513561025e10d9c9637e3f9b44687e5)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e8fb56da298578ca8d39c9c724261d97457df5b34e852a54598f6ca319976a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="campaignHook")
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.CampaignHookProperty"]]:
        '''The settings for the Lambda function to use by default as a code hook for campaigns in the application.

        To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-campaignhook
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.CampaignHookProperty"]], jsii.get(self, "campaignHook"))

    @campaign_hook.setter
    def campaign_hook(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.CampaignHookProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74976d0ff12837f5338928827e51fb9c721668e97e7428ddf1dc20485880b56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "campaignHook", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchMetricsEnabled")
    def cloud_watch_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable application-related alarms in Amazon CloudWatch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-cloudwatchmetricsenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "cloudWatchMetricsEnabled"))

    @cloud_watch_metrics_enabled.setter
    def cloud_watch_metrics_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c45868d9d830dab662d4e5882d69b5cbf3567bef5e727946d301776193bd3d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchMetricsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.LimitsProperty"]]:
        '''The default sending limits for campaigns in the application.

        To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-limits
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.LimitsProperty"]], jsii.get(self, "limits"))

    @limits.setter
    def limits(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.LimitsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3bb5b9589b8d6052708702f064d21841b15fce11748395a8f9a03db14ccd634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value)

    @builtins.property
    @jsii.member(jsii_name="quietTime")
    def quiet_time(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.QuietTimeProperty"]]:
        '''The default quiet time for campaigns in the application.

        Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met:

        - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value.
        - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings).
        - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings).

        If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled.

        To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-quiettime
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.QuietTimeProperty"]], jsii.get(self, "quietTime"))

    @quiet_time.setter
    def quiet_time(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationSettings.QuietTimeProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0596480f4edc84656225446717bc11b496418f6149b5df27ae0c961d32ee0a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quietTime", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnApplicationSettings.CampaignHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_name": "lambdaFunctionName",
            "mode": "mode",
            "web_url": "webUrl",
        },
    )
    class CampaignHookProperty:
        def __init__(
            self,
            *,
            lambda_function_name: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            web_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Lambda function to use by default as a code hook for campaigns in the application.

            :param lambda_function_name: The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to send messages for campaigns in the application.
            :param mode: The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:. - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign. - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.
            :param web_url: The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                campaign_hook_property = pinpoint.CfnApplicationSettings.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e92f57ddd653aa16dba3f02196d1f66b04f83e5b03fa202375cb584fa114a63)
                check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument web_url", value=web_url, expected_type=type_hints["web_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if mode is not None:
                self._values["mode"] = mode
            if web_url is not None:
                self._values["web_url"] = web_url

        @builtins.property
        def lambda_function_name(self) -> typing.Optional[builtins.str]:
            '''The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to send messages for campaigns in the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-lambdafunctionname
            '''
            result = self._values.get("lambda_function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:.

            - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign.
            - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def web_url(self) -> typing.Optional[builtins.str]:
            '''The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-weburl
            '''
            result = self._values.get("web_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnApplicationSettings.LimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "maximum_duration": "maximumDuration",
            "messages_per_second": "messagesPerSecond",
            "total": "total",
        },
    )
    class LimitsProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[jsii.Number] = None,
            maximum_duration: typing.Optional[jsii.Number] = None,
            messages_per_second: typing.Optional[jsii.Number] = None,
            total: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the default sending limits for campaigns in the application.

            :param daily: The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period. The maximum value is 100.
            :param maximum_duration: The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign. The minimum value is 60 seconds.
            :param messages_per_second: The maximum number of messages that a campaign can send each second. The minimum value is 50. The maximum value is 20,000.
            :param total: The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign. The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                limits_property = pinpoint.CfnApplicationSettings.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    total=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1fd4b78bc4370a1e61236d8e16f00207cf1ee14ee038f1540751d8991636ccd1)
                check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
                check_type(argname="argument maximum_duration", value=maximum_duration, expected_type=type_hints["maximum_duration"])
                check_type(argname="argument messages_per_second", value=messages_per_second, expected_type=type_hints["messages_per_second"])
                check_type(argname="argument total", value=total, expected_type=type_hints["total"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if maximum_duration is not None:
                self._values["maximum_duration"] = maximum_duration
            if messages_per_second is not None:
                self._values["messages_per_second"] = messages_per_second
            if total is not None:
                self._values["total"] = total

        @builtins.property
        def daily(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period.

            The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-daily
            '''
            result = self._values.get("daily")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_duration(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign.

            The minimum value is 60 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-maximumduration
            '''
            result = self._values.get("maximum_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def messages_per_second(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send each second.

            The minimum value is 50. The maximum value is 20,000.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-messagespersecond
            '''
            result = self._values.get("messages_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign.

            The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-total
            '''
            result = self._values.get("total")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnApplicationSettings.QuietTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class QuietTimeProperty:
        def __init__(self, *, end: builtins.str, start: builtins.str) -> None:
            '''Specifies the start and end times that define a time range when messages aren't sent to endpoints.

            :param end: The specific time when quiet time ends. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.
            :param start: The specific time when quiet time begins. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                quiet_time_property = pinpoint.CfnApplicationSettings.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__967e7415ae200a01b9ddb4f52f65a8ac594028cec75d8637eefeb659e62a862e)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "end": end,
                "start": start,
            }

        @builtins.property
        def end(self) -> builtins.str:
            '''The specific time when quiet time ends.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html#cfn-pinpoint-applicationsettings-quiettime-end
            '''
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def start(self) -> builtins.str:
            '''The specific time when quiet time begins.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html#cfn-pinpoint-applicationsettings-quiettime-start
            '''
            result = self._values.get("start")
            assert result is not None, "Required property 'start' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuietTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnApplicationSettingsProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "campaign_hook": "campaignHook",
        "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
        "limits": "limits",
        "quiet_time": "quietTime",
    },
)
class CfnApplicationSettingsProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        campaign_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        limits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.LimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        quiet_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplicationSettings``.

        :param application_id: The unique identifier for the Amazon Pinpoint application.
        :param campaign_hook: The settings for the Lambda function to use by default as a code hook for campaigns in the application. To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.
        :param cloud_watch_metrics_enabled: Specifies whether to enable application-related alarms in Amazon CloudWatch.
        :param limits: The default sending limits for campaigns in the application. To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.
        :param quiet_time: The default quiet time for campaigns in the application. Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met: - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value. - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings). - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings). If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled. To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_application_settings_props = pinpoint.CfnApplicationSettingsProps(
                application_id="applicationId",
            
                # the properties below are optional
                campaign_hook=pinpoint.CfnApplicationSettings.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                ),
                cloud_watch_metrics_enabled=False,
                limits=pinpoint.CfnApplicationSettings.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    total=123
                ),
                quiet_time=pinpoint.CfnApplicationSettings.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4d4d3fb7dea08b491541e3b25658722b92ae0c1965b3a4b8a6cb694ae65245)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument campaign_hook", value=campaign_hook, expected_type=type_hints["campaign_hook"])
            check_type(argname="argument cloud_watch_metrics_enabled", value=cloud_watch_metrics_enabled, expected_type=type_hints["cloud_watch_metrics_enabled"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument quiet_time", value=quiet_time, expected_type=type_hints["quiet_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if campaign_hook is not None:
            self._values["campaign_hook"] = campaign_hook
        if cloud_watch_metrics_enabled is not None:
            self._values["cloud_watch_metrics_enabled"] = cloud_watch_metrics_enabled
        if limits is not None:
            self._values["limits"] = limits
        if quiet_time is not None:
            self._values["quiet_time"] = quiet_time

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.CampaignHookProperty]]:
        '''The settings for the Lambda function to use by default as a code hook for campaigns in the application.

        To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-campaignhook
        '''
        result = self._values.get("campaign_hook")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.CampaignHookProperty]], result)

    @builtins.property
    def cloud_watch_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable application-related alarms in Amazon CloudWatch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-cloudwatchmetricsenabled
        '''
        result = self._values.get("cloud_watch_metrics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.LimitsProperty]]:
        '''The default sending limits for campaigns in the application.

        To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-limits
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.LimitsProperty]], result)

    @builtins.property
    def quiet_time(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.QuietTimeProperty]]:
        '''The default quiet time for campaigns in the application.

        Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met:

        - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value.
        - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings).
        - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings).

        If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled.

        To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-quiettime
        '''
        result = self._values.get("quiet_time")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.QuietTimeProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationSettingsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnBaiduChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnBaiduChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::BaiduChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the Baidu channel to send notifications to the Baidu Cloud Push notification service. Before you can use Amazon Pinpoint to send notifications to the Baidu Cloud Push service, you have to enable the Baidu channel for an Amazon Pinpoint application.

    The BaiduChannel resource represents the status and authentication settings of the Baidu channel for an application.

    :cloudformationResource: AWS::Pinpoint::BaiduChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_baidu_channel = pinpoint.CfnBaiduChannel(self, "MyCfnBaiduChannel",
            api_key="apiKey",
            application_id="applicationId",
            secret_key="secretKey",
        
            # the properties below are optional
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        secret_key: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::BaiduChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key: The API key that you received from the Baidu Cloud Push service to communicate with the service.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.
        :param secret_key: The secret key that you received from the Baidu Cloud Push service to communicate with the service.
        :param enabled: Specifies whether to enable the Baidu channel for the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e4017fb957107ef8edfac95ebf5b2c89d8de19ee66002f32583e24c05715f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBaiduChannelProps(
            api_key=api_key,
            application_id=application_id,
            secret_key=secret_key,
            enabled=enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9623bf6b3a79eb66f3076d81ee282f245d20577ee5b663dd9b3fb98eb3835d8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5225e971f544ea5ab60cbef67dc740c41f3b34609a8c4fa2df06264c3e4319f7)
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
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        '''The API key that you received from the Baidu Cloud Push service to communicate with the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-apikey
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58453759e3455ec47c00b3d46c422ff22d72834dc9b0b0162b1d0942c539161b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value)

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95629246d13954f399a65391512c09dc9e7221851a80d123429457f3021868d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        '''The secret key that you received from the Baidu Cloud Push service to communicate with the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-secretkey
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c680b38c8525862cd812eaa73e1ba790ae155f40b4fd698335bd022cd85816db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the Baidu channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9df32be297a3d2b631fc1217d6fd36e99182f2a0aab77905d148978f445d18f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnBaiduChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_id": "applicationId",
        "secret_key": "secretKey",
        "enabled": "enabled",
    },
)
class CfnBaiduChannelProps:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        secret_key: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnBaiduChannel``.

        :param api_key: The API key that you received from the Baidu Cloud Push service to communicate with the service.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.
        :param secret_key: The secret key that you received from the Baidu Cloud Push service to communicate with the service.
        :param enabled: Specifies whether to enable the Baidu channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_baidu_channel_props = pinpoint.CfnBaiduChannelProps(
                api_key="apiKey",
                application_id="applicationId",
                secret_key="secretKey",
            
                # the properties below are optional
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9c40921b2a9b6d7761eed64f65ef3fc23a95a7afdd25bb6e960e74f3b73213)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "application_id": application_id,
            "secret_key": secret_key,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def api_key(self) -> builtins.str:
        '''The API key that you received from the Baidu Cloud Push service to communicate with the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-apikey
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_key(self) -> builtins.str:
        '''The secret key that you received from the Baidu Cloud Push service to communicate with the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-secretkey
        '''
        result = self._values.get("secret_key")
        assert result is not None, "Required property 'secret_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the Baidu channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBaiduChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCampaign(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign",
):
    '''A CloudFormation ``AWS::Pinpoint::Campaign``.

    Specifies the settings for a campaign. A *campaign* is a messaging initiative that engages a specific segment of users for an Amazon Pinpoint application.

    :cloudformationResource: AWS::Pinpoint::Campaign
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        # attributes: Any
        # custom_config: Any
        # metrics: Any
        # tags: Any
        
        cfn_campaign = pinpoint.CfnCampaign(self, "MyCfnCampaign",
            application_id="applicationId",
            name="name",
            schedule=pinpoint.CfnCampaign.ScheduleProperty(
                end_time="endTime",
                event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                    dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                        attributes=attributes,
                        event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        metrics=metrics
                    ),
                    filter_type="filterType"
                ),
                frequency="frequency",
                is_local_time=False,
                quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                    end="end",
                    start="start"
                ),
                start_time="startTime",
                time_zone="timeZone"
            ),
            segment_id="segmentId",
        
            # the properties below are optional
            additional_treatments=[pinpoint.CfnCampaign.WriteTreatmentResourceProperty(
                custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                ),
                message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                    adm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                        content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                ),
                schedule=pinpoint.CfnCampaign.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                        dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                ),
                size_percent=123,
                template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                    email_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    )
                ),
                treatment_description="treatmentDescription",
                treatment_name="treatmentName"
            )],
            campaign_hook=pinpoint.CfnCampaign.CampaignHookProperty(
                lambda_function_name="lambdaFunctionName",
                mode="mode",
                web_url="webUrl"
            ),
            custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                delivery_uri="deliveryUri",
                endpoint_types=["endpointTypes"]
            ),
            description="description",
            holdout_percent=123,
            is_paused=False,
            limits=pinpoint.CfnCampaign.LimitsProperty(
                daily=123,
                maximum_duration=123,
                messages_per_second=123,
                session=123,
                total=123
            ),
            message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                adm_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                apns_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                baidu_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                    data="data"
                ),
                default_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                    body="body",
                    from_address="fromAddress",
                    html_body="htmlBody",
                    title="title"
                ),
                gcm_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                    content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                        background_color="backgroundColor",
                        body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                            alignment="alignment",
                            body="body",
                            text_color="textColor"
                        ),
                        header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                            alignment="alignment",
                            header="header",
                            text_color="textColor"
                        ),
                        image_url="imageUrl",
                        primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                            android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        ),
                        secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                            android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        )
                    )],
                    custom_config=custom_config,
                    layout="layout"
                ),
                sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                    body="body",
                    entity_id="entityId",
                    message_type="messageType",
                    origination_number="originationNumber",
                    sender_id="senderId",
                    template_id="templateId"
                )
            ),
            priority=123,
            segment_version=123,
            tags=tags,
            template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                email_template=pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                ),
                push_template=pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                ),
                sms_template=pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                ),
                voice_template=pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                )
            ),
            treatment_description="treatmentDescription",
            treatment_name="treatmentName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        name: builtins.str,
        schedule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]],
        segment_id: builtins.str,
        additional_treatments: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.WriteTreatmentResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        campaign_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.CampaignHookProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        holdout_percent: typing.Optional[jsii.Number] = None,
        is_paused: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        limits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.LimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        message_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.MessageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        segment_version: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        template_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.TemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        treatment_description: typing.Optional[builtins.str] = None,
        treatment_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::Campaign``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the campaign is associated with.
        :param name: The name of the campaign.
        :param schedule: The schedule settings for the campaign.
        :param segment_id: The unique identifier for the segment to associate with the campaign.
        :param additional_treatments: An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.
        :param campaign_hook: Specifies the Lambda function to use as a code hook for a campaign.
        :param custom_delivery_configuration: The delivery configuration settings for sending the treatment through a custom channel. This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.
        :param description: A custom description of the campaign.
        :param holdout_percent: The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.
        :param is_paused: Specifies whether to pause the campaign. A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it.
        :param limits: The messaging limits for the campaign.
        :param message_configuration: The message configuration settings for the campaign.
        :param priority: An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest. If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.
        :param segment_version: The version of the segment to associate with the campaign.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_configuration: The message template to use for the treatment.
        :param treatment_description: A custom description of the default treatment for the campaign.
        :param treatment_name: A custom name of the default treatment for the campaign, if the campaign has multiple treatments. A *treatment* is a variation of a campaign that's used for A/B testing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f312ba8488922bb988cded7e2490b7e0c6ed68b18df08cd55e88808792af98)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCampaignProps(
            application_id=application_id,
            name=name,
            schedule=schedule,
            segment_id=segment_id,
            additional_treatments=additional_treatments,
            campaign_hook=campaign_hook,
            custom_delivery_configuration=custom_delivery_configuration,
            description=description,
            holdout_percent=holdout_percent,
            is_paused=is_paused,
            limits=limits,
            message_configuration=message_configuration,
            priority=priority,
            segment_version=segment_version,
            tags=tags,
            template_configuration=template_configuration,
            treatment_description=treatment_description,
            treatment_name=treatment_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0510e5453252f5aca1d2efa74566a0d6621d348a3ac30242190a550eb9097cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f68ceef6f72b6889db39a0aae149934397474ea3d4375ba596546bb52fe3550a)
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
        '''The Amazon Resource Name (ARN) of the campaign.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCampaignId")
    def attr_campaign_id(self) -> builtins.str:
        '''The unique identifier for the campaign.

        :cloudformationAttribute: CampaignId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCampaignId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the campaign is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a00b8f96c494829d8216144ce316931f8b9cc2a1af20690ae3c17fb6802b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9f23cd386851b7432c427c076f1b740dcf28cd3ab21a3746e2c24d242ff7ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.ScheduleProperty"]:
        '''The schedule settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-schedule
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.ScheduleProperty"], jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.ScheduleProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402dae6387dcbcf9d244bfe777309bd4a3732a876f78c1c2943a3be60ab3bd4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="segmentId")
    def segment_id(self) -> builtins.str:
        '''The unique identifier for the segment to associate with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentid
        '''
        return typing.cast(builtins.str, jsii.get(self, "segmentId"))

    @segment_id.setter
    def segment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8197fa413cff5a608e0931a0adf3dcd51fd4d24dc28913cf1c20ef9cefcacf8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentId", value)

    @builtins.property
    @jsii.member(jsii_name="additionalTreatments")
    def additional_treatments(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.WriteTreatmentResourceProperty"]]]]:
        '''An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-additionaltreatments
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.WriteTreatmentResourceProperty"]]]], jsii.get(self, "additionalTreatments"))

    @additional_treatments.setter
    def additional_treatments(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.WriteTreatmentResourceProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468639b5b0aecd36e6bafd0d020bc48cc5e5f1918afdcf195393dae29c116112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalTreatments", value)

    @builtins.property
    @jsii.member(jsii_name="campaignHook")
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignHookProperty"]]:
        '''Specifies the Lambda function to use as a code hook for a campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-campaignhook
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignHookProperty"]], jsii.get(self, "campaignHook"))

    @campaign_hook.setter
    def campaign_hook(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignHookProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b70a1a55856d85013ddc9a9c020bcc5397da9ab3656a14a0cf656d1367c541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "campaignHook", value)

    @builtins.property
    @jsii.member(jsii_name="customDeliveryConfiguration")
    def custom_delivery_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CustomDeliveryConfigurationProperty"]]:
        '''The delivery configuration settings for sending the treatment through a custom channel.

        This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-customdeliveryconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CustomDeliveryConfigurationProperty"]], jsii.get(self, "customDeliveryConfiguration"))

    @custom_delivery_configuration.setter
    def custom_delivery_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CustomDeliveryConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d279c867d043711677cf90da2bf24804a0460b310eb1f972fe551778b46fa9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDeliveryConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c80e19e37274cc6145ac6078d0d44dd4360008ef903f541c7ae53f26bcf327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="holdoutPercent")
    def holdout_percent(self) -> typing.Optional[jsii.Number]:
        '''The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-holdoutpercent
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "holdoutPercent"))

    @holdout_percent.setter
    def holdout_percent(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c21aa521d6b2340c52a6e0e57eb31979397dca86456d0812004fa834e05d0cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "holdoutPercent", value)

    @builtins.property
    @jsii.member(jsii_name="isPaused")
    def is_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to pause the campaign.

        A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-ispaused
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "isPaused"))

    @is_paused.setter
    def is_paused(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bdb83ae5e091ddcb7ca324e504556a0293d978c1e1a51757c11f032306e77b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPaused", value)

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.LimitsProperty"]]:
        '''The messaging limits for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-limits
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.LimitsProperty"]], jsii.get(self, "limits"))

    @limits.setter
    def limits(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.LimitsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fc5294b0429581a813a969789c4c2ce6c779ab82519995d04a129429fd9879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value)

    @builtins.property
    @jsii.member(jsii_name="messageConfiguration")
    def message_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageConfigurationProperty"]]:
        '''The message configuration settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-messageconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageConfigurationProperty"]], jsii.get(self, "messageConfiguration"))

    @message_configuration.setter
    def message_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67aaefe46d0e026926b19b1f92238defe75978a3656316bb5bc4033ea1484a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> typing.Optional[jsii.Number]:
        '''An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest.

        If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-priority
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b915814949b0b9cba117adb87e309d6ea45a0b929fe82ca4179feb80d1f1fbad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="segmentVersion")
    def segment_version(self) -> typing.Optional[jsii.Number]:
        '''The version of the segment to associate with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentversion
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "segmentVersion"))

    @segment_version.setter
    def segment_version(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6347a994a4952dcd1174bb33aeee26f672afa001b878d34e0f8e1d33167d783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentVersion", value)

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    def template_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateConfigurationProperty"]]:
        '''The message template to use for the treatment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-templateconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateConfigurationProperty"]], jsii.get(self, "templateConfiguration"))

    @template_configuration.setter
    def template_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690875121b95ffea809005b44a64172ca545deff9c710ee3590f873abd080fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="treatmentDescription")
    def treatment_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the default treatment for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "treatmentDescription"))

    @treatment_description.setter
    def treatment_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0206bc47b41e759bb57da8f33eaceb37065ed5c326107ef8c237d94548ebc3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "treatmentDescription", value)

    @builtins.property
    @jsii.member(jsii_name="treatmentName")
    def treatment_name(self) -> typing.Optional[builtins.str]:
        '''A custom name of the default treatment for the campaign, if the campaign has multiple treatments.

        A *treatment* is a variation of a campaign that's used for A/B testing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "treatmentName"))

    @treatment_name.setter
    def treatment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d476178f7d3414340ac6392d0c5382b456c08e882f5547e02ffa7d68c8eae23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "treatmentName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.AttributeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_type": "attributeType", "values": "values"},
    )
    class AttributeDimensionProperty:
        def __init__(
            self,
            *,
            attribute_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies attribute-based criteria for including or excluding endpoints from a segment.

            :param attribute_type: The type of segment dimension to use. Valid values are:. - ``INCLUSIVE`` – endpoints that have attributes matching the values are included in the segment. - ``EXCLUSIVE`` – endpoints that have attributes matching the values are excluded from the segment. - ``CONTAINS`` – endpoints that have attributes' substrings match the values are included in the segment. - ``BEFORE`` – endpoints with attributes read as ISO_INSTANT datetimes before the value are included in the segment. - ``AFTER`` – endpoints with attributes read as ISO_INSTANT datetimes after the value are included in the segment. - ``BETWEEN`` – endpoints with attributes read as ISO_INSTANT datetimes between the values are included in the segment. - ``ON`` – endpoints with attributes read as ISO_INSTANT dates on the value are included in the segment. Time is ignored in this comparison.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``AttributeType`` property, endpoints are included or excluded from the segment if their attribute values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                attribute_dimension_property = pinpoint.CfnCampaign.AttributeDimensionProperty(
                    attribute_type="attributeType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4251d500dfda9df0d13af3b53dc2a58e7c18f9eb84171c7302cf20ef8fc3b209)
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use. Valid values are:.

            - ``INCLUSIVE`` – endpoints that have attributes matching the values are included in the segment.
            - ``EXCLUSIVE`` – endpoints that have attributes matching the values are excluded from the segment.
            - ``CONTAINS`` – endpoints that have attributes' substrings match the values are included in the segment.
            - ``BEFORE`` – endpoints with attributes read as ISO_INSTANT datetimes before the value are included in the segment.
            - ``AFTER`` – endpoints with attributes read as ISO_INSTANT datetimes after the value are included in the segment.
            - ``BETWEEN`` – endpoints with attributes read as ISO_INSTANT datetimes between the values are included in the segment.
            - ``ON`` – endpoints with attributes read as ISO_INSTANT dates on the value are included in the segment. Time is ignored in this comparison.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html#cfn-pinpoint-campaign-attributedimension-attributetype
            '''
            result = self._values.get("attribute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``AttributeType`` property, endpoints are included or excluded from the segment if their attribute values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html#cfn-pinpoint-campaign-attributedimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.CampaignCustomMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"data": "data"},
    )
    class CampaignCustomMessageProperty:
        def __init__(self, *, data: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the contents of a message that's sent through a custom channel to recipients of a campaign.

            :param data: The raw, JSON-formatted string to use as the payload for the message. The maximum size is 5 KB.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigncustommessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                campaign_custom_message_property = pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6f3c5aa5c1d54a20fd1891660410759a3bad3d7d80c8ed6b4661cf8aca9fc8f)
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data is not None:
                self._values["data"] = data

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''The raw, JSON-formatted string to use as the payload for the message.

            The maximum size is 5 KB.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigncustommessage.html#cfn-pinpoint-campaign-campaigncustommessage-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignCustomMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.CampaignEmailMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body": "body",
            "from_address": "fromAddress",
            "html_body": "htmlBody",
            "title": "title",
        },
    )
    class CampaignEmailMessageProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[builtins.str] = None,
            from_address: typing.Optional[builtins.str] = None,
            html_body: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and "From" address for an email message that's sent to recipients of a campaign.

            :param body: The body of the email for recipients whose email clients don't render HTML content.
            :param from_address: The verified email address to send the email from. The default address is the ``FromAddress`` specified for the email channel for the application.
            :param html_body: The body of the email, in HTML format, for recipients whose email clients render HTML content.
            :param title: The subject line, or title, of the email.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                campaign_email_message_property = pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                    body="body",
                    from_address="fromAddress",
                    html_body="htmlBody",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f154ba157a4e14cc3e9c26384ba9e0c70c6170ffc9b304789bb167d11c13faa)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument from_address", value=from_address, expected_type=type_hints["from_address"])
                check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if from_address is not None:
                self._values["from_address"] = from_address
            if html_body is not None:
                self._values["html_body"] = html_body
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the email for recipients whose email clients don't render HTML content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def from_address(self) -> typing.Optional[builtins.str]:
            '''The verified email address to send the email from.

            The default address is the ``FromAddress`` specified for the email channel for the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-fromaddress
            '''
            result = self._values.get("from_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def html_body(self) -> typing.Optional[builtins.str]:
            '''The body of the email, in HTML format, for recipients whose email clients render HTML content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-htmlbody
            '''
            result = self._values.get("html_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The subject line, or title, of the email.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignEmailMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.CampaignEventFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions", "filter_type": "filterType"},
    )
    class CampaignEventFilterProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.EventDimensionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the settings for events that cause a campaign to be sent.

            :param dimensions: The dimension settings of the event filter for the campaign.
            :param filter_type: The type of event that causes the campaign to be sent. Valid values are: ``SYSTEM`` , sends the campaign when a system event occurs; and, ``ENDPOINT`` , sends the campaign when an endpoint event (Events resource) occurs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                
                campaign_event_filter_property = pinpoint.CfnCampaign.CampaignEventFilterProperty(
                    dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                        attributes=attributes,
                        event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        metrics=metrics
                    ),
                    filter_type="filterType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9bcf71d57091f65f8a430d19e4d41879a49ab3dc5b5d89878c469fe03e4d01b8)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if filter_type is not None:
                self._values["filter_type"] = filter_type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.EventDimensionsProperty"]]:
            '''The dimension settings of the event filter for the campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html#cfn-pinpoint-campaign-campaigneventfilter-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.EventDimensionsProperty"]], result)

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The type of event that causes the campaign to be sent.

            Valid values are: ``SYSTEM`` , sends the campaign when a system event occurs; and, ``ENDPOINT`` , sends the campaign when an endpoint event (Events resource) occurs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html#cfn-pinpoint-campaign-campaigneventfilter-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignEventFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.CampaignHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_name": "lambdaFunctionName",
            "mode": "mode",
            "web_url": "webUrl",
        },
    )
    class CampaignHookProperty:
        def __init__(
            self,
            *,
            lambda_function_name: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            web_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies settings for invoking an Lambda function that customizes a segment for a campaign.

            :param lambda_function_name: The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to customize a segment for a campaign.
            :param mode: The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:. - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign. - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.
            :param web_url: The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                campaign_hook_property = pinpoint.CfnCampaign.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0991cfc3a3c4ffb7cafef1e0b8af172a82e348cc02f536fae664d444a0393912)
                check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument web_url", value=web_url, expected_type=type_hints["web_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if mode is not None:
                self._values["mode"] = mode
            if web_url is not None:
                self._values["web_url"] = web_url

        @builtins.property
        def lambda_function_name(self) -> typing.Optional[builtins.str]:
            '''The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to customize a segment for a campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-lambdafunctionname
            '''
            result = self._values.get("lambda_function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:.

            - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign.
            - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def web_url(self) -> typing.Optional[builtins.str]:
            '''The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-weburl
            '''
            result = self._values.get("web_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.CampaignInAppMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content": "content",
            "custom_config": "customConfig",
            "layout": "layout",
        },
    )
    class CampaignInAppMessageProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.InAppMessageContentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_config: typing.Any = None,
            layout: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the appearance of an in-app message, including the message type, the title and body text, text and background colors, and the configurations of buttons that appear in the message.

            :param content: An array that contains configurtion information about the in-app message for the campaign, including title and body text, text colors, background colors, image URLs, and button configurations.
            :param custom_config: Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.
            :param layout: A string that describes how the in-app message will appear. You can specify one of the following:. - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page. - ``TOP_BANNER`` – a message that appears as a banner at the top of the page. - ``OVERLAYS`` – a message that covers entire screen. - ``MOBILE_FEED`` – a message that appears in a window in front of the page. - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page. - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # custom_config: Any
                
                campaign_in_app_message_property = pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                    content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                        background_color="backgroundColor",
                        body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                            alignment="alignment",
                            body="body",
                            text_color="textColor"
                        ),
                        header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                            alignment="alignment",
                            header="header",
                            text_color="textColor"
                        ),
                        image_url="imageUrl",
                        primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                            android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        ),
                        secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                            android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        )
                    )],
                    custom_config=custom_config,
                    layout="layout"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88ad29224e0ae089c0e96535955dbbd2bf1ce9804daa612f3d30056d4db01cb5)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
                check_type(argname="argument layout", value=layout, expected_type=type_hints["layout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if custom_config is not None:
                self._values["custom_config"] = custom_config
            if layout is not None:
                self._values["layout"] = layout

        @builtins.property
        def content(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageContentProperty"]]]]:
            '''An array that contains configurtion information about the in-app message for the campaign, including title and body text, text colors, background colors, image URLs, and button configurations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageContentProperty"]]]], result)

        @builtins.property
        def custom_config(self) -> typing.Any:
            '''Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-customconfig
            '''
            result = self._values.get("custom_config")
            return typing.cast(typing.Any, result)

        @builtins.property
        def layout(self) -> typing.Optional[builtins.str]:
            '''A string that describes how the in-app message will appear. You can specify one of the following:.

            - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page.
            - ``TOP_BANNER`` – a message that appears as a banner at the top of the page.
            - ``OVERLAYS`` – a message that covers entire screen.
            - ``MOBILE_FEED`` – a message that appears in a window in front of the page.
            - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page.
            - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-layout
            '''
            result = self._values.get("layout")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignInAppMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.CampaignSmsMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body": "body",
            "entity_id": "entityId",
            "message_type": "messageType",
            "origination_number": "originationNumber",
            "sender_id": "senderId",
            "template_id": "templateId",
        },
    )
    class CampaignSmsMessageProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[builtins.str] = None,
            entity_id: typing.Optional[builtins.str] = None,
            message_type: typing.Optional[builtins.str] = None,
            origination_number: typing.Optional[builtins.str] = None,
            sender_id: typing.Optional[builtins.str] = None,
            template_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and settings for an SMS message that's sent to recipients of a campaign.

            :param body: The body of the SMS message.
            :param entity_id: The entity ID or Principal Entity (PE) id received from the regulatory body for sending SMS in your country.
            :param message_type: The SMS message type. Valid values are ``TRANSACTIONAL`` (for messages that are critical or time-sensitive, such as a one-time passwords) and ``PROMOTIONAL`` (for messsages that aren't critical or time-sensitive, such as marketing messages).
            :param origination_number: The long code to send the SMS message from. This value should be one of the dedicated long codes that's assigned to your AWS account. Although it isn't required, we recommend that you specify the long code using an E.164 format to ensure prompt and accurate delivery of the message. For example, +12065550100.
            :param sender_id: The alphabetic Sender ID to display as the sender of the message on a recipient's device. Support for sender IDs varies by country or region. To specify a phone number as the sender, omit this parameter and use ``OriginationNumber`` instead. For more information about support for Sender ID by country, see the `Amazon Pinpoint User Guide <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ .
            :param template_id: The template ID received from the regulatory body for sending SMS in your country.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                campaign_sms_message_property = pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                    body="body",
                    entity_id="entityId",
                    message_type="messageType",
                    origination_number="originationNumber",
                    sender_id="senderId",
                    template_id="templateId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__155eded46e7c94a5a9dd5f0964941d0c297f5d9db7a94349b034c6edfcef7be1)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
                check_type(argname="argument message_type", value=message_type, expected_type=type_hints["message_type"])
                check_type(argname="argument origination_number", value=origination_number, expected_type=type_hints["origination_number"])
                check_type(argname="argument sender_id", value=sender_id, expected_type=type_hints["sender_id"])
                check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if entity_id is not None:
                self._values["entity_id"] = entity_id
            if message_type is not None:
                self._values["message_type"] = message_type
            if origination_number is not None:
                self._values["origination_number"] = origination_number
            if sender_id is not None:
                self._values["sender_id"] = sender_id
            if template_id is not None:
                self._values["template_id"] = template_id

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the SMS message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entity_id(self) -> typing.Optional[builtins.str]:
            '''The entity ID or Principal Entity (PE) id received from the regulatory body for sending SMS in your country.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-entityid
            '''
            result = self._values.get("entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_type(self) -> typing.Optional[builtins.str]:
            '''The SMS message type.

            Valid values are ``TRANSACTIONAL`` (for messages that are critical or time-sensitive, such as a one-time passwords) and ``PROMOTIONAL`` (for messsages that aren't critical or time-sensitive, such as marketing messages).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-messagetype
            '''
            result = self._values.get("message_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def origination_number(self) -> typing.Optional[builtins.str]:
            '''The long code to send the SMS message from.

            This value should be one of the dedicated long codes that's assigned to your AWS account. Although it isn't required, we recommend that you specify the long code using an E.164 format to ensure prompt and accurate delivery of the message. For example, +12065550100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-originationnumber
            '''
            result = self._values.get("origination_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sender_id(self) -> typing.Optional[builtins.str]:
            '''The alphabetic Sender ID to display as the sender of the message on a recipient's device.

            Support for sender IDs varies by country or region. To specify a phone number as the sender, omit this parameter and use ``OriginationNumber`` instead. For more information about support for Sender ID by country, see the `Amazon Pinpoint User Guide <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-senderid
            '''
            result = self._values.get("sender_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def template_id(self) -> typing.Optional[builtins.str]:
            '''The template ID received from the regulatory body for sending SMS in your country.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-templateid
            '''
            result = self._values.get("template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignSmsMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_uri": "deliveryUri",
            "endpoint_types": "endpointTypes",
        },
    )
    class CustomDeliveryConfigurationProperty:
        def __init__(
            self,
            *,
            delivery_uri: typing.Optional[builtins.str] = None,
            endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the delivery configuration settings for sending a campaign or campaign treatment through a custom channel.

            This object is required if you use the ``CampaignCustomMessage`` object to define the message to send for the campaign or campaign treatment.

            :param delivery_uri: The destination to send the campaign or treatment to. This value can be one of the following:. - The name or Amazon Resource Name (ARN) of an AWS Lambda function to invoke to handle delivery of the campaign or treatment. - The URL for a web application or service that supports HTTPS and can receive the message. The URL has to be a full URL, including the HTTPS protocol.
            :param endpoint_types: The types of endpoints to send the campaign or treatment to. Each valid value maps to a type of channel that you can associate with an endpoint by using the ``ChannelType`` property of an endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                custom_delivery_configuration_property = pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e8feab8abce0f08277c847a660a7ec8980b62f1d7aea8bb7157677d2d744fae)
                check_type(argname="argument delivery_uri", value=delivery_uri, expected_type=type_hints["delivery_uri"])
                check_type(argname="argument endpoint_types", value=endpoint_types, expected_type=type_hints["endpoint_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_uri is not None:
                self._values["delivery_uri"] = delivery_uri
            if endpoint_types is not None:
                self._values["endpoint_types"] = endpoint_types

        @builtins.property
        def delivery_uri(self) -> typing.Optional[builtins.str]:
            '''The destination to send the campaign or treatment to. This value can be one of the following:.

            - The name or Amazon Resource Name (ARN) of an AWS Lambda function to invoke to handle delivery of the campaign or treatment.
            - The URL for a web application or service that supports HTTPS and can receive the message. The URL has to be a full URL, including the HTTPS protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html#cfn-pinpoint-campaign-customdeliveryconfiguration-deliveryuri
            '''
            result = self._values.get("delivery_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The types of endpoints to send the campaign or treatment to.

            Each valid value maps to a type of channel that you can associate with an endpoint by using the ``ChannelType`` property of an endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html#cfn-pinpoint-campaign-customdeliveryconfiguration-endpointtypes
            '''
            result = self._values.get("endpoint_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomDeliveryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.DefaultButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "border_radius": "borderRadius",
            "button_action": "buttonAction",
            "link": "link",
            "text": "text",
            "text_color": "textColor",
        },
    )
    class DefaultButtonConfigurationProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            border_radius: typing.Optional[jsii.Number] = None,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
            text: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default behavior for a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :param background_color: The background color of a button, expressed as a hex color code (such as #000000 for black).
            :param border_radius: The border radius of a button.
            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.
            :param text: The text that appears on a button in an in-app message.
            :param text_color: The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                default_button_configuration_property = pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                    background_color="backgroundColor",
                    border_radius=123,
                    button_action="buttonAction",
                    link="link",
                    text="text",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__08fcc3214998024dd043dce3cf9d2a66a6f95040bf12731bed23ed76489a9903)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument border_radius", value=border_radius, expected_type=type_hints["border_radius"])
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if border_radius is not None:
                self._values["border_radius"] = border_radius
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link
            if text is not None:
                self._values["text"] = text
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color of a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def border_radius(self) -> typing.Optional[jsii.Number]:
            '''The border radius of a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-borderradius
            '''
            result = self._values.get("border_radius")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text that appears on a button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.EventDimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "event_type": "eventType",
            "metrics": "metrics",
        },
    )
    class EventDimensionsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            event_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metrics: typing.Any = None,
        ) -> None:
            '''Specifies the dimensions for an event filter that determines when a campaign is sent or a journey activity is performed.

            :param attributes: One or more custom attributes that your application reports to Amazon Pinpoint. You can use these attributes as selection criteria when you create an event filter.
            :param event_type: The name of the event that causes the campaign to be sent or the journey activity to be performed. This can be a standard event that Amazon Pinpoint generates, such as ``_email.delivered`` or ``_custom.delivered`` . For campaigns, this can also be a custom event that's specific to your application. For information about standard events, see `Streaming Amazon Pinpoint Events <https://docs.aws.amazon.com/pinpoint/latest/developerguide/event-streams.html>`_ in the *Amazon Pinpoint Developer Guide* .
            :param metrics: One or more custom metrics that your application reports to Amazon Pinpoint . You can use these metrics as selection criteria when you create an event filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                
                event_dimensions_property = pinpoint.CfnCampaign.EventDimensionsProperty(
                    attributes=attributes,
                    event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    metrics=metrics
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12848ac9df7b383d00d6225849ef7982e3726e8f4b1e10ea95e90307de1e7f05)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if event_type is not None:
                self._values["event_type"] = event_type
            if metrics is not None:
                self._values["metrics"] = metrics

        @builtins.property
        def attributes(self) -> typing.Any:
            '''One or more custom attributes that your application reports to Amazon Pinpoint.

            You can use these attributes as selection criteria when you create an event filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.SetDimensionProperty"]]:
            '''The name of the event that causes the campaign to be sent or the journey activity to be performed.

            This can be a standard event that Amazon Pinpoint generates, such as ``_email.delivered`` or ``_custom.delivered`` . For campaigns, this can also be a custom event that's specific to your application. For information about standard events, see `Streaming Amazon Pinpoint Events <https://docs.aws.amazon.com/pinpoint/latest/developerguide/event-streams.html>`_ in the *Amazon Pinpoint Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-eventtype
            '''
            result = self._values.get("event_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.SetDimensionProperty"]], result)

        @builtins.property
        def metrics(self) -> typing.Any:
            '''One or more custom metrics that your application reports to Amazon Pinpoint .

            You can use these metrics as selection criteria when you create an event filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventDimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.InAppMessageBodyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "body": "body",
            "text_color": "textColor",
        },
    )
    class InAppMessageBodyConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of main body text of the in-app message.

            :param alignment: The text alignment of the main body text of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param body: The main body text of the message.
            :param text_color: The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                in_app_message_body_config_property = pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__798f78d2a50cdcae6b4b93b8977132f8bda3d8dc3a7ef93a5d4f5e5d9c55f4b0)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if body is not None:
                self._values["body"] = body
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the main body text of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The main body text of the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageBodyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.InAppMessageButtonProperty",
        jsii_struct_bases=[],
        name_mapping={
            "android": "android",
            "default_config": "defaultConfig",
            "ios": "ios",
            "web": "web",
        },
    )
    class InAppMessageButtonProperty:
        def __init__(
            self,
            *,
            android: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.DefaultButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ios: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            web: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration of a button that appears in an in-app message.

            :param android: An object that defines the default behavior for a button in in-app messages sent to Android.
            :param default_config: An object that defines the default behavior for a button in an in-app message.
            :param ios: An object that defines the default behavior for a button in in-app messages sent to iOS devices.
            :param web: An object that defines the default behavior for a button in in-app messages for web applications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                in_app_message_button_property = pinpoint.CfnCampaign.InAppMessageButtonProperty(
                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca2acb8ebbfd23d801d4081a1e6f915a455fa8cc9851e8604710d576f7f10afd)
                check_type(argname="argument android", value=android, expected_type=type_hints["android"])
                check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
                check_type(argname="argument ios", value=ios, expected_type=type_hints["ios"])
                check_type(argname="argument web", value=web, expected_type=type_hints["web"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if android is not None:
                self._values["android"] = android
            if default_config is not None:
                self._values["default_config"] = default_config
            if ios is not None:
                self._values["ios"] = ios
            if web is not None:
                self._values["web"] = web

        @builtins.property
        def android(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OverrideButtonConfigurationProperty"]]:
            '''An object that defines the default behavior for a button in in-app messages sent to Android.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-android
            '''
            result = self._values.get("android")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OverrideButtonConfigurationProperty"]], result)

        @builtins.property
        def default_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.DefaultButtonConfigurationProperty"]]:
            '''An object that defines the default behavior for a button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-defaultconfig
            '''
            result = self._values.get("default_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.DefaultButtonConfigurationProperty"]], result)

        @builtins.property
        def ios(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OverrideButtonConfigurationProperty"]]:
            '''An object that defines the default behavior for a button in in-app messages sent to iOS devices.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-ios
            '''
            result = self._values.get("ios")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OverrideButtonConfigurationProperty"]], result)

        @builtins.property
        def web(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OverrideButtonConfigurationProperty"]]:
            '''An object that defines the default behavior for a button in in-app messages for web applications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-web
            '''
            result = self._values.get("web")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OverrideButtonConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageButtonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.InAppMessageContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "body_config": "bodyConfig",
            "header_config": "headerConfig",
            "image_url": "imageUrl",
            "primary_btn": "primaryBtn",
            "secondary_btn": "secondaryBtn",
        },
    )
    class InAppMessageContentProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            body_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.InAppMessageBodyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            header_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.InAppMessageHeaderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_url: typing.Optional[builtins.str] = None,
            primary_btn: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.InAppMessageButtonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secondary_btn: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.InAppMessageButtonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration and contents of an in-app message.

            :param background_color: The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).
            :param body_config: Specifies the configuration of main body text in an in-app message template.
            :param header_config: Specifies the configuration and content of the header or title text of the in-app message.
            :param image_url: The URL of the image that appears on an in-app message banner.
            :param primary_btn: An object that contains configuration information about the primary button in an in-app message.
            :param secondary_btn: An object that contains configuration information about the secondary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                in_app_message_content_property = pinpoint.CfnCampaign.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                        android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                        android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc1cf923fc276b77b363db06c8a5ccddd5dac458124e77d29786fe78ce8f5f7e)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument body_config", value=body_config, expected_type=type_hints["body_config"])
                check_type(argname="argument header_config", value=header_config, expected_type=type_hints["header_config"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument primary_btn", value=primary_btn, expected_type=type_hints["primary_btn"])
                check_type(argname="argument secondary_btn", value=secondary_btn, expected_type=type_hints["secondary_btn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if body_config is not None:
                self._values["body_config"] = body_config
            if header_config is not None:
                self._values["header_config"] = header_config
            if image_url is not None:
                self._values["image_url"] = image_url
            if primary_btn is not None:
                self._values["primary_btn"] = primary_btn
            if secondary_btn is not None:
                self._values["secondary_btn"] = secondary_btn

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageBodyConfigProperty"]]:
            '''Specifies the configuration of main body text in an in-app message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-bodyconfig
            '''
            result = self._values.get("body_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageBodyConfigProperty"]], result)

        @builtins.property
        def header_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageHeaderConfigProperty"]]:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-headerconfig
            '''
            result = self._values.get("header_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageHeaderConfigProperty"]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image that appears on an in-app message banner.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_btn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageButtonProperty"]]:
            '''An object that contains configuration information about the primary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-primarybtn
            '''
            result = self._values.get("primary_btn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageButtonProperty"]], result)

        @builtins.property
        def secondary_btn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageButtonProperty"]]:
            '''An object that contains configuration information about the secondary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-secondarybtn
            '''
            result = self._values.get("secondary_btn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.InAppMessageButtonProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "header": "header",
            "text_color": "textColor",
        },
    )
    class InAppMessageHeaderConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            header: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :param alignment: The text alignment of the title of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param header: The header or title text of the in-app message.
            :param text_color: The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                in_app_message_header_config_property = pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a9de89d0e96f2ce72a8e1c85f8a5c8c1b829c2e831625f1ce68c1a35f420aef)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if header is not None:
                self._values["header"] = header
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the title of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header(self) -> typing.Optional[builtins.str]:
            '''The header or title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-header
            '''
            result = self._values.get("header")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.LimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "maximum_duration": "maximumDuration",
            "messages_per_second": "messagesPerSecond",
            "session": "session",
            "total": "total",
        },
    )
    class LimitsProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[jsii.Number] = None,
            maximum_duration: typing.Optional[jsii.Number] = None,
            messages_per_second: typing.Optional[jsii.Number] = None,
            session: typing.Optional[jsii.Number] = None,
            total: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the limits on the messages that a campaign can send.

            :param daily: The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period. The maximum value is 100.
            :param maximum_duration: The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign. The minimum value is 60 seconds.
            :param messages_per_second: The maximum number of messages that a campaign can send each second. The minimum value is 50. The maximum value is 20,000.
            :param session: ``CfnCampaign.LimitsProperty.Session``.
            :param total: The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign. The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                limits_property = pinpoint.CfnCampaign.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    session=123,
                    total=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__547273fb7d7d1dadd3428718b6a46ca495cf2fbebd24e52c67312c91f82a2098)
                check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
                check_type(argname="argument maximum_duration", value=maximum_duration, expected_type=type_hints["maximum_duration"])
                check_type(argname="argument messages_per_second", value=messages_per_second, expected_type=type_hints["messages_per_second"])
                check_type(argname="argument session", value=session, expected_type=type_hints["session"])
                check_type(argname="argument total", value=total, expected_type=type_hints["total"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if maximum_duration is not None:
                self._values["maximum_duration"] = maximum_duration
            if messages_per_second is not None:
                self._values["messages_per_second"] = messages_per_second
            if session is not None:
                self._values["session"] = session
            if total is not None:
                self._values["total"] = total

        @builtins.property
        def daily(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period.

            The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-daily
            '''
            result = self._values.get("daily")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_duration(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign.

            The minimum value is 60 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-maximumduration
            '''
            result = self._values.get("maximum_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def messages_per_second(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send each second.

            The minimum value is 50. The maximum value is 20,000.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-messagespersecond
            '''
            result = self._values.get("messages_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def session(self) -> typing.Optional[jsii.Number]:
            '''``CfnCampaign.LimitsProperty.Session``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-session
            '''
            result = self._values.get("session")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign.

            The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-total
            '''
            result = self._values.get("total")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.MessageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "adm_message": "admMessage",
            "apns_message": "apnsMessage",
            "baidu_message": "baiduMessage",
            "custom_message": "customMessage",
            "default_message": "defaultMessage",
            "email_message": "emailMessage",
            "gcm_message": "gcmMessage",
            "in_app_message": "inAppMessage",
            "sms_message": "smsMessage",
        },
    )
    class MessageConfigurationProperty:
        def __init__(
            self,
            *,
            adm_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            apns_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            baidu_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.CampaignCustomMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            email_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.CampaignEmailMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            gcm_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            in_app_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.CampaignInAppMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sms_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.CampaignSmsMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the message configuration settings for a campaign.

            :param adm_message: The message that the campaign sends through the ADM (Amazon Device Messaging) channel. If specified, this message overrides the default message.
            :param apns_message: The message that the campaign sends through the APNs (Apple Push Notification service) channel. If specified, this message overrides the default message.
            :param baidu_message: The message that the campaign sends through the Baidu (Baidu Cloud Push) channel. If specified, this message overrides the default message.
            :param custom_message: The message that the campaign sends through a custom channel, as specified by the delivery configuration ( ``CustomDeliveryConfiguration`` ) settings for the campaign. If specified, this message overrides the default message.
            :param default_message: The default message that the campaign sends through all the channels that are configured for the campaign.
            :param email_message: The message that the campaign sends through the email channel. If specified, this message overrides the default message.
            :param gcm_message: The message that the campaign sends through the GCM channel, which enables Amazon Pinpoint to send push notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service. If specified, this message overrides the default message.
            :param in_app_message: The default message for the in-app messaging channel. This message overrides the default message ( ``DefaultMessage`` ).
            :param sms_message: The message that the campaign sends through the SMS channel. If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # custom_config: Any
                
                message_configuration_property = pinpoint.CfnCampaign.MessageConfigurationProperty(
                    adm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                        content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__673029b1d2b3b7b9f6ba109a03b7a73f7f5c7bea38d170bac99e720941e9022c)
                check_type(argname="argument adm_message", value=adm_message, expected_type=type_hints["adm_message"])
                check_type(argname="argument apns_message", value=apns_message, expected_type=type_hints["apns_message"])
                check_type(argname="argument baidu_message", value=baidu_message, expected_type=type_hints["baidu_message"])
                check_type(argname="argument custom_message", value=custom_message, expected_type=type_hints["custom_message"])
                check_type(argname="argument default_message", value=default_message, expected_type=type_hints["default_message"])
                check_type(argname="argument email_message", value=email_message, expected_type=type_hints["email_message"])
                check_type(argname="argument gcm_message", value=gcm_message, expected_type=type_hints["gcm_message"])
                check_type(argname="argument in_app_message", value=in_app_message, expected_type=type_hints["in_app_message"])
                check_type(argname="argument sms_message", value=sms_message, expected_type=type_hints["sms_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if adm_message is not None:
                self._values["adm_message"] = adm_message
            if apns_message is not None:
                self._values["apns_message"] = apns_message
            if baidu_message is not None:
                self._values["baidu_message"] = baidu_message
            if custom_message is not None:
                self._values["custom_message"] = custom_message
            if default_message is not None:
                self._values["default_message"] = default_message
            if email_message is not None:
                self._values["email_message"] = email_message
            if gcm_message is not None:
                self._values["gcm_message"] = gcm_message
            if in_app_message is not None:
                self._values["in_app_message"] = in_app_message
            if sms_message is not None:
                self._values["sms_message"] = sms_message

        @builtins.property
        def adm_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]]:
            '''The message that the campaign sends through the ADM (Amazon Device Messaging) channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-admmessage
            '''
            result = self._values.get("adm_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]], result)

        @builtins.property
        def apns_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]]:
            '''The message that the campaign sends through the APNs (Apple Push Notification service) channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-apnsmessage
            '''
            result = self._values.get("apns_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]], result)

        @builtins.property
        def baidu_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]]:
            '''The message that the campaign sends through the Baidu (Baidu Cloud Push) channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-baidumessage
            '''
            result = self._values.get("baidu_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]], result)

        @builtins.property
        def custom_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignCustomMessageProperty"]]:
            '''The message that the campaign sends through a custom channel, as specified by the delivery configuration ( ``CustomDeliveryConfiguration`` ) settings for the campaign.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-custommessage
            '''
            result = self._values.get("custom_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignCustomMessageProperty"]], result)

        @builtins.property
        def default_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]]:
            '''The default message that the campaign sends through all the channels that are configured for the campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-defaultmessage
            '''
            result = self._values.get("default_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]], result)

        @builtins.property
        def email_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignEmailMessageProperty"]]:
            '''The message that the campaign sends through the email channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-emailmessage
            '''
            result = self._values.get("email_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignEmailMessageProperty"]], result)

        @builtins.property
        def gcm_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]]:
            '''The message that the campaign sends through the GCM channel, which enables Amazon Pinpoint to send push notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-gcmmessage
            '''
            result = self._values.get("gcm_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageProperty"]], result)

        @builtins.property
        def in_app_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignInAppMessageProperty"]]:
            '''The default message for the in-app messaging channel.

            This message overrides the default message ( ``DefaultMessage`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-inappmessage
            '''
            result = self._values.get("in_app_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignInAppMessageProperty"]], result)

        @builtins.property
        def sms_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignSmsMessageProperty"]]:
            '''The message that the campaign sends through the SMS channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-smsmessage
            '''
            result = self._values.get("sms_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignSmsMessageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.MessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "image_icon_url": "imageIconUrl",
            "image_small_icon_url": "imageSmallIconUrl",
            "image_url": "imageUrl",
            "json_body": "jsonBody",
            "media_url": "mediaUrl",
            "raw_content": "rawContent",
            "silent_push": "silentPush",
            "time_to_live": "timeToLive",
            "title": "title",
            "url": "url",
        },
    )
    class MessageProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            image_icon_url: typing.Optional[builtins.str] = None,
            image_small_icon_url: typing.Optional[builtins.str] = None,
            image_url: typing.Optional[builtins.str] = None,
            json_body: typing.Optional[builtins.str] = None,
            media_url: typing.Optional[builtins.str] = None,
            raw_content: typing.Optional[builtins.str] = None,
            silent_push: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            time_to_live: typing.Optional[jsii.Number] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and settings for a push notification that's sent to recipients of a campaign.

            :param action: The action to occur if a recipient taps the push notification. Valid values are:. - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of iOS and Android. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The body of the notification message. The maximum number of characters is 200.
            :param image_icon_url: The URL of the image to display as the push notification icon, such as the icon for the app.
            :param image_small_icon_url: The URL of the image to display as the small, push notification icon, such as a small version of the icon for the app.
            :param image_url: The URL of an image to display in the push notification.
            :param json_body: The JSON payload to use for a silent push notification.
            :param media_url: The URL of the image or video to display in the push notification.
            :param raw_content: The raw, JSON-formatted string to use as the payload for the notification message. If specified, this value overrides all other content for the message.
            :param silent_push: Specifies whether the notification is a silent push notification, which is a push notification that doesn't display on a recipient's device. Silent push notifications can be used for cases such as updating an app's configuration, displaying messages in an in-app message center, or supporting phone home functionality.
            :param time_to_live: The number of seconds that the push notification service should keep the message, if the service is unable to deliver the notification the first time. This value is converted to an expiration value when it's sent to a push notification service. If this value is ``0`` , the service treats the notification as if it expires immediately and the service doesn't store or try to deliver the notification again. This value doesn't apply to messages that are sent through the Amazon Device Messaging (ADM) service.
            :param title: The title to display above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps the push notification and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                message_property = pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2bc34013a62c0edc5a6f214411224d49e050250647a3a82b79757fe56202b12)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument image_icon_url", value=image_icon_url, expected_type=type_hints["image_icon_url"])
                check_type(argname="argument image_small_icon_url", value=image_small_icon_url, expected_type=type_hints["image_small_icon_url"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument json_body", value=json_body, expected_type=type_hints["json_body"])
                check_type(argname="argument media_url", value=media_url, expected_type=type_hints["media_url"])
                check_type(argname="argument raw_content", value=raw_content, expected_type=type_hints["raw_content"])
                check_type(argname="argument silent_push", value=silent_push, expected_type=type_hints["silent_push"])
                check_type(argname="argument time_to_live", value=time_to_live, expected_type=type_hints["time_to_live"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if image_icon_url is not None:
                self._values["image_icon_url"] = image_icon_url
            if image_small_icon_url is not None:
                self._values["image_small_icon_url"] = image_small_icon_url
            if image_url is not None:
                self._values["image_url"] = image_url
            if json_body is not None:
                self._values["json_body"] = json_body
            if media_url is not None:
                self._values["media_url"] = media_url
            if raw_content is not None:
                self._values["raw_content"] = raw_content
            if silent_push is not None:
                self._values["silent_push"] = silent_push
            if time_to_live is not None:
                self._values["time_to_live"] = time_to_live
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps the push notification. Valid values are:.

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of iOS and Android.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the notification message.

            The maximum number of characters is 200.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image to display as the push notification icon, such as the icon for the app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imageiconurl
            '''
            result = self._values.get("image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_small_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image to display as the small, push notification icon, such as a small version of the icon for the app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imagesmalliconurl
            '''
            result = self._values.get("image_small_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image to display in the push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def json_body(self) -> typing.Optional[builtins.str]:
            '''The JSON payload to use for a silent push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-jsonbody
            '''
            result = self._values.get("json_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def media_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image or video to display in the push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-mediaurl
            '''
            result = self._values.get("media_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def raw_content(self) -> typing.Optional[builtins.str]:
            '''The raw, JSON-formatted string to use as the payload for the notification message.

            If specified, this value overrides all other content for the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-rawcontent
            '''
            result = self._values.get("raw_content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def silent_push(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether the notification is a silent push notification, which is a push notification that doesn't display on a recipient's device.

            Silent push notifications can be used for cases such as updating an app's configuration, displaying messages in an in-app message center, or supporting phone home functionality.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-silentpush
            '''
            result = self._values.get("silent_push")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def time_to_live(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds that the push notification service should keep the message, if the service is unable to deliver the notification the first time.

            This value is converted to an expiration value when it's sent to a push notification service. If this value is ``0`` , the service treats the notification as if it expires immediately and the service doesn't store or try to deliver the notification again.

            This value doesn't apply to messages that are sent through the Amazon Device Messaging (ADM) service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-timetolive
            '''
            result = self._values.get("time_to_live")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to display above the notification message on a recipient's device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps the push notification and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison_operator": "comparisonOperator", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies metric-based criteria for including or excluding endpoints from a segment.

            These criteria derive from custom metrics that you define for endpoints.

            :param comparison_operator: The operator to use when comparing metric values. Valid values are: ``GREATER_THAN`` , ``LESS_THAN`` , ``GREATER_THAN_OR_EQUAL`` , ``LESS_THAN_OR_EQUAL`` , and ``EQUAL`` .
            :param value: The value to compare.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                metric_dimension_property = pinpoint.CfnCampaign.MetricDimensionProperty(
                    comparison_operator="comparisonOperator",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99f3a5a251a9e03a3edca9a530106a058940f030b6387c1c9bf5e5f178f57950)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''The operator to use when comparing metric values.

            Valid values are: ``GREATER_THAN`` , ``LESS_THAN`` , ``GREATER_THAN_OR_EQUAL`` , ``LESS_THAN_OR_EQUAL`` , and ``EQUAL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html#cfn-pinpoint-campaign-metricdimension-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value to compare.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html#cfn-pinpoint-campaign-metricdimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.OverrideButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"button_action": "buttonAction", "link": "link"},
    )
    class OverrideButtonConfigurationProperty:
        def __init__(
            self,
            *,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of a button with settings that are specific to a certain device type.

            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                override_button_configuration_property = pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                    button_action="buttonAction",
                    link="link"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a095a94fc2a3f5f02c4bee6a6379e008774c3379ff92ccc90d393056c433c86e)
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html#cfn-pinpoint-campaign-overridebuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html#cfn-pinpoint-campaign-overridebuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.QuietTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class QuietTimeProperty:
        def __init__(self, *, end: builtins.str, start: builtins.str) -> None:
            '''Specifies the start and end times that define a time range when messages aren't sent to endpoints.

            :param end: The specific time when quiet time ends. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.
            :param start: The specific time when quiet time begins. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                quiet_time_property = pinpoint.CfnCampaign.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2bddb3dc8424c9ff4650617fab4a715388f3cbc41ddc77bd8d174a6bdafbdfc1)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "end": end,
                "start": start,
            }

        @builtins.property
        def end(self) -> builtins.str:
            '''The specific time when quiet time ends.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html#cfn-pinpoint-campaign-schedule-quiettime-end
            '''
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def start(self) -> builtins.str:
            '''The specific time when quiet time begins.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html#cfn-pinpoint-campaign-schedule-quiettime-start
            '''
            result = self._values.get("start")
            assert result is not None, "Required property 'start' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuietTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_time": "endTime",
            "event_filter": "eventFilter",
            "frequency": "frequency",
            "is_local_time": "isLocalTime",
            "quiet_time": "quietTime",
            "start_time": "startTime",
            "time_zone": "timeZone",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[builtins.str] = None,
            event_filter: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.CampaignEventFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            frequency: typing.Optional[builtins.str] = None,
            is_local_time: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            quiet_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.QuietTimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            start_time: typing.Optional[builtins.str] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the schedule settings for a campaign.

            :param end_time: The scheduled time, in ISO 8601 format, when the campaign ended or will end.
            :param event_filter: The type of event that causes the campaign to be sent, if the value of the ``Frequency`` property is ``EVENT`` .
            :param frequency: Specifies how often the campaign is sent or whether the campaign is sent in response to a specific event.
            :param is_local_time: Specifies whether the start and end times for the campaign schedule use each recipient's local time. To base the schedule on each recipient's local time, set this value to ``true`` .
            :param quiet_time: The default quiet time for the campaign. Quiet time is a specific time range when a campaign doesn't send messages to endpoints, if all the following conditions are met: - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value. - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the campaign. - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the campaign. If any of the preceding conditions isn't met, the endpoint will receive messages from the campaign, even if quiet time is enabled.
            :param start_time: The scheduled time when the campaign began or will begin. Valid values are: ``IMMEDIATE`` , to start the campaign immediately; or, a specific time in ISO 8601 format.
            :param time_zone: The starting UTC offset for the campaign schedule, if the value of the ``IsLocalTime`` property is ``true`` . Valid values are: ``UTC, UTC+01, UTC+02, UTC+03, UTC+03:30, UTC+04, UTC+04:30, UTC+05, UTC+05:30, UTC+05:45, UTC+06, UTC+06:30, UTC+07, UTC+08, UTC+09, UTC+09:30, UTC+10, UTC+10:30, UTC+11, UTC+12, UTC+13, UTC-02, UTC-03, UTC-04, UTC-05, UTC-06, UTC-07, UTC-08, UTC-09, UTC-10,`` and ``UTC-11`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                
                schedule_property = pinpoint.CfnCampaign.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                        dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a28328c02ca2d5803d7b94a649e1731518fd6571b2a3d476f0d52b1eaab811cd)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
                check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
                check_type(argname="argument is_local_time", value=is_local_time, expected_type=type_hints["is_local_time"])
                check_type(argname="argument quiet_time", value=quiet_time, expected_type=type_hints["quiet_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if event_filter is not None:
                self._values["event_filter"] = event_filter
            if frequency is not None:
                self._values["frequency"] = frequency
            if is_local_time is not None:
                self._values["is_local_time"] = is_local_time
            if quiet_time is not None:
                self._values["quiet_time"] = quiet_time
            if start_time is not None:
                self._values["start_time"] = start_time
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def end_time(self) -> typing.Optional[builtins.str]:
            '''The scheduled time, in ISO 8601 format, when the campaign ended or will end.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignEventFilterProperty"]]:
            '''The type of event that causes the campaign to be sent, if the value of the ``Frequency`` property is ``EVENT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-eventfilter
            '''
            result = self._values.get("event_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CampaignEventFilterProperty"]], result)

        @builtins.property
        def frequency(self) -> typing.Optional[builtins.str]:
            '''Specifies how often the campaign is sent or whether the campaign is sent in response to a specific event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-frequency
            '''
            result = self._values.get("frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_local_time(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether the start and end times for the campaign schedule use each recipient's local time.

            To base the schedule on each recipient's local time, set this value to ``true`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-islocaltime
            '''
            result = self._values.get("is_local_time")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def quiet_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.QuietTimeProperty"]]:
            '''The default quiet time for the campaign.

            Quiet time is a specific time range when a campaign doesn't send messages to endpoints, if all the following conditions are met:

            - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value.
            - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the campaign.
            - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the campaign.

            If any of the preceding conditions isn't met, the endpoint will receive messages from the campaign, even if quiet time is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-quiettime
            '''
            result = self._values.get("quiet_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.QuietTimeProperty"]], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''The scheduled time when the campaign began or will begin.

            Valid values are: ``IMMEDIATE`` , to start the campaign immediately; or, a specific time in ISO 8601 format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            '''The starting UTC offset for the campaign schedule, if the value of the ``IsLocalTime`` property is ``true`` .

            Valid values are: ``UTC, UTC+01, UTC+02, UTC+03, UTC+03:30, UTC+04, UTC+04:30, UTC+05, UTC+05:30, UTC+05:45, UTC+06, UTC+06:30, UTC+07, UTC+08, UTC+09, UTC+09:30, UTC+10, UTC+10:30, UTC+11, UTC+12, UTC+13, UTC-02, UTC-03, UTC-04, UTC-05, UTC-06, UTC-07, UTC-08, UTC-09, UTC-10,`` and ``UTC-11`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-timezone
            '''
            result = self._values.get("time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.SetDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class SetDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the dimension type and values for a segment dimension.

            :param dimension_type: The type of segment dimension to use. Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                set_dimension_property = pinpoint.CfnCampaign.SetDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62820699c46cf6118cb37ad264ac6bd74634ff8ac16df06981f6fda8bb10c8b1)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use.

            Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html#cfn-pinpoint-campaign-setdimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html#cfn-pinpoint-campaign-setdimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.TemplateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email_template": "emailTemplate",
            "push_template": "pushTemplate",
            "sms_template": "smsTemplate",
            "voice_template": "voiceTemplate",
        },
    )
    class TemplateConfigurationProperty:
        def __init__(
            self,
            *,
            email_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            push_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sms_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            voice_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the message template to use for the message, for each type of channel.

            :param email_template: The email template to use for the message.
            :param push_template: The push notification template to use for the message.
            :param sms_template: The SMS template to use for the message.
            :param voice_template: The voice template to use for the message. This object isn't supported for campaigns.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                template_configuration_property = pinpoint.CfnCampaign.TemplateConfigurationProperty(
                    email_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff680b114ac7eb3301e3ca9e3c054a07877c14dcee79f62b145a3323d877f717)
                check_type(argname="argument email_template", value=email_template, expected_type=type_hints["email_template"])
                check_type(argname="argument push_template", value=push_template, expected_type=type_hints["push_template"])
                check_type(argname="argument sms_template", value=sms_template, expected_type=type_hints["sms_template"])
                check_type(argname="argument voice_template", value=voice_template, expected_type=type_hints["voice_template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_template is not None:
                self._values["email_template"] = email_template
            if push_template is not None:
                self._values["push_template"] = push_template
            if sms_template is not None:
                self._values["sms_template"] = sms_template
            if voice_template is not None:
                self._values["voice_template"] = voice_template

        @builtins.property
        def email_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateProperty"]]:
            '''The email template to use for the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-emailtemplate
            '''
            result = self._values.get("email_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateProperty"]], result)

        @builtins.property
        def push_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateProperty"]]:
            '''The push notification template to use for the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-pushtemplate
            '''
            result = self._values.get("push_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateProperty"]], result)

        @builtins.property
        def sms_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateProperty"]]:
            '''The SMS template to use for the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-smstemplate
            '''
            result = self._values.get("sms_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateProperty"]], result)

        @builtins.property
        def voice_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateProperty"]]:
            '''The voice template to use for the message.

            This object isn't supported for campaigns.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-voicetemplate
            '''
            result = self._values.get("voice_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.TemplateProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class TemplateProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the name and version of the message template to use for the message.

            :param name: The name of the message template to use for the message. If specified, this value must match the name of an existing message template.
            :param version: The unique identifier for the version of the message template to use for the message. If specified, this value must match the identifier for an existing template version. To retrieve a list of versions and version identifiers for a template, use the Template Versions resource. If you don't specify a value for this property, Amazon Pinpoint uses the *active version* of the template. The *active version* is typically the version of a template that's been most recently reviewed and approved for use, depending on your workflow. It isn't necessarily the latest version of a template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                template_property = pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51544243cac2e8deda2d5e6e42909b0810bb720b60bf05558129962396b6c511)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the message template to use for the message.

            If specified, this value must match the name of an existing message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html#cfn-pinpoint-campaign-template-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the version of the message template to use for the message.

            If specified, this value must match the identifier for an existing template version. To retrieve a list of versions and version identifiers for a template, use the Template Versions resource.

            If you don't specify a value for this property, Amazon Pinpoint uses the *active version* of the template. The *active version* is typically the version of a template that's been most recently reviewed and approved for use, depending on your workflow. It isn't necessarily the latest version of a template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html#cfn-pinpoint-campaign-template-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnCampaign.WriteTreatmentResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_delivery_configuration": "customDeliveryConfiguration",
            "message_configuration": "messageConfiguration",
            "schedule": "schedule",
            "size_percent": "sizePercent",
            "template_configuration": "templateConfiguration",
            "treatment_description": "treatmentDescription",
            "treatment_name": "treatmentName",
        },
    )
    class WriteTreatmentResourceProperty:
        def __init__(
            self,
            *,
            custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            message_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.MessageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schedule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            size_percent: typing.Optional[jsii.Number] = None,
            template_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.TemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            treatment_description: typing.Optional[builtins.str] = None,
            treatment_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the settings for a campaign treatment.

            A *treatment* is a variation of a campaign that's used for A/B testing of a campaign.

            :param custom_delivery_configuration: The delivery configuration settings for sending the treatment through a custom channel. This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.
            :param message_configuration: The message configuration settings for the treatment.
            :param schedule: The schedule settings for the treatment.
            :param size_percent: The allocated percentage of users (segment members) to send the treatment to.
            :param template_configuration: The message template to use for the treatment.
            :param treatment_description: A custom description of the treatment.
            :param treatment_name: A custom name for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # attributes: Any
                # custom_config: Any
                # metrics: Any
                
                write_treatment_resource_property = pinpoint.CfnCampaign.WriteTreatmentResourceProperty(
                    custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                        delivery_uri="deliveryUri",
                        endpoint_types=["endpointTypes"]
                    ),
                    message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                        adm_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        apns_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        baidu_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                            data="data"
                        ),
                        default_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                            body="body",
                            from_address="fromAddress",
                            html_body="htmlBody",
                            title="title"
                        ),
                        gcm_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                            content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                                background_color="backgroundColor",
                                body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                    alignment="alignment",
                                    body="body",
                                    text_color="textColor"
                                ),
                                header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                    alignment="alignment",
                                    header="header",
                                    text_color="textColor"
                                ),
                                image_url="imageUrl",
                                primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                ),
                                secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                )
                            )],
                            custom_config=custom_config,
                            layout="layout"
                        ),
                        sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                            body="body",
                            entity_id="entityId",
                            message_type="messageType",
                            origination_number="originationNumber",
                            sender_id="senderId",
                            template_id="templateId"
                        )
                    ),
                    schedule=pinpoint.CfnCampaign.ScheduleProperty(
                        end_time="endTime",
                        event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                            dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                                attributes=attributes,
                                event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                metrics=metrics
                            ),
                            filter_type="filterType"
                        ),
                        frequency="frequency",
                        is_local_time=False,
                        quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                            end="end",
                            start="start"
                        ),
                        start_time="startTime",
                        time_zone="timeZone"
                    ),
                    size_percent=123,
                    template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                        email_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        push_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        sms_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        voice_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        )
                    ),
                    treatment_description="treatmentDescription",
                    treatment_name="treatmentName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0c287844519a3aec1773ace90dda6f6b00bb3d979c7b90db154d5f19df47bad)
                check_type(argname="argument custom_delivery_configuration", value=custom_delivery_configuration, expected_type=type_hints["custom_delivery_configuration"])
                check_type(argname="argument message_configuration", value=message_configuration, expected_type=type_hints["message_configuration"])
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument size_percent", value=size_percent, expected_type=type_hints["size_percent"])
                check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
                check_type(argname="argument treatment_description", value=treatment_description, expected_type=type_hints["treatment_description"])
                check_type(argname="argument treatment_name", value=treatment_name, expected_type=type_hints["treatment_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_delivery_configuration is not None:
                self._values["custom_delivery_configuration"] = custom_delivery_configuration
            if message_configuration is not None:
                self._values["message_configuration"] = message_configuration
            if schedule is not None:
                self._values["schedule"] = schedule
            if size_percent is not None:
                self._values["size_percent"] = size_percent
            if template_configuration is not None:
                self._values["template_configuration"] = template_configuration
            if treatment_description is not None:
                self._values["treatment_description"] = treatment_description
            if treatment_name is not None:
                self._values["treatment_name"] = treatment_name

        @builtins.property
        def custom_delivery_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CustomDeliveryConfigurationProperty"]]:
            '''The delivery configuration settings for sending the treatment through a custom channel.

            This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-customdeliveryconfiguration
            '''
            result = self._values.get("custom_delivery_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.CustomDeliveryConfigurationProperty"]], result)

        @builtins.property
        def message_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageConfigurationProperty"]]:
            '''The message configuration settings for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-messageconfiguration
            '''
            result = self._values.get("message_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.MessageConfigurationProperty"]], result)

        @builtins.property
        def schedule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.ScheduleProperty"]]:
            '''The schedule settings for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.ScheduleProperty"]], result)

        @builtins.property
        def size_percent(self) -> typing.Optional[jsii.Number]:
            '''The allocated percentage of users (segment members) to send the treatment to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-sizepercent
            '''
            result = self._values.get("size_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def template_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateConfigurationProperty"]]:
            '''The message template to use for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-templateconfiguration
            '''
            result = self._values.get("template_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.TemplateConfigurationProperty"]], result)

        @builtins.property
        def treatment_description(self) -> typing.Optional[builtins.str]:
            '''A custom description of the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-treatmentdescription
            '''
            result = self._values.get("treatment_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def treatment_name(self) -> typing.Optional[builtins.str]:
            '''A custom name for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-treatmentname
            '''
            result = self._values.get("treatment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WriteTreatmentResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnCampaignProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "name": "name",
        "schedule": "schedule",
        "segment_id": "segmentId",
        "additional_treatments": "additionalTreatments",
        "campaign_hook": "campaignHook",
        "custom_delivery_configuration": "customDeliveryConfiguration",
        "description": "description",
        "holdout_percent": "holdoutPercent",
        "is_paused": "isPaused",
        "limits": "limits",
        "message_configuration": "messageConfiguration",
        "priority": "priority",
        "segment_version": "segmentVersion",
        "tags": "tags",
        "template_configuration": "templateConfiguration",
        "treatment_description": "treatmentDescription",
        "treatment_name": "treatmentName",
    },
)
class CfnCampaignProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        name: builtins.str,
        schedule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]],
        segment_id: builtins.str,
        additional_treatments: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.WriteTreatmentResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        campaign_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        holdout_percent: typing.Optional[jsii.Number] = None,
        is_paused: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        limits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.LimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        message_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        segment_version: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        template_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        treatment_description: typing.Optional[builtins.str] = None,
        treatment_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCampaign``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the campaign is associated with.
        :param name: The name of the campaign.
        :param schedule: The schedule settings for the campaign.
        :param segment_id: The unique identifier for the segment to associate with the campaign.
        :param additional_treatments: An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.
        :param campaign_hook: Specifies the Lambda function to use as a code hook for a campaign.
        :param custom_delivery_configuration: The delivery configuration settings for sending the treatment through a custom channel. This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.
        :param description: A custom description of the campaign.
        :param holdout_percent: The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.
        :param is_paused: Specifies whether to pause the campaign. A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it.
        :param limits: The messaging limits for the campaign.
        :param message_configuration: The message configuration settings for the campaign.
        :param priority: An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest. If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.
        :param segment_version: The version of the segment to associate with the campaign.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_configuration: The message template to use for the treatment.
        :param treatment_description: A custom description of the default treatment for the campaign.
        :param treatment_name: A custom name of the default treatment for the campaign, if the campaign has multiple treatments. A *treatment* is a variation of a campaign that's used for A/B testing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            # attributes: Any
            # custom_config: Any
            # metrics: Any
            # tags: Any
            
            cfn_campaign_props = pinpoint.CfnCampaignProps(
                application_id="applicationId",
                name="name",
                schedule=pinpoint.CfnCampaign.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                        dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                ),
                segment_id="segmentId",
            
                # the properties below are optional
                additional_treatments=[pinpoint.CfnCampaign.WriteTreatmentResourceProperty(
                    custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                        delivery_uri="deliveryUri",
                        endpoint_types=["endpointTypes"]
                    ),
                    message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                        adm_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        apns_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        baidu_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                            data="data"
                        ),
                        default_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                            body="body",
                            from_address="fromAddress",
                            html_body="htmlBody",
                            title="title"
                        ),
                        gcm_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                            content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                                background_color="backgroundColor",
                                body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                    alignment="alignment",
                                    body="body",
                                    text_color="textColor"
                                ),
                                header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                    alignment="alignment",
                                    header="header",
                                    text_color="textColor"
                                ),
                                image_url="imageUrl",
                                primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                ),
                                secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                )
                            )],
                            custom_config=custom_config,
                            layout="layout"
                        ),
                        sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                            body="body",
                            entity_id="entityId",
                            message_type="messageType",
                            origination_number="originationNumber",
                            sender_id="senderId",
                            template_id="templateId"
                        )
                    ),
                    schedule=pinpoint.CfnCampaign.ScheduleProperty(
                        end_time="endTime",
                        event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                            dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                                attributes=attributes,
                                event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                metrics=metrics
                            ),
                            filter_type="filterType"
                        ),
                        frequency="frequency",
                        is_local_time=False,
                        quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                            end="end",
                            start="start"
                        ),
                        start_time="startTime",
                        time_zone="timeZone"
                    ),
                    size_percent=123,
                    template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                        email_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        push_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        sms_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        voice_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        )
                    ),
                    treatment_description="treatmentDescription",
                    treatment_name="treatmentName"
                )],
                campaign_hook=pinpoint.CfnCampaign.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                ),
                custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                ),
                description="description",
                holdout_percent=123,
                is_paused=False,
                limits=pinpoint.CfnCampaign.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    session=123,
                    total=123
                ),
                message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                    adm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                        content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                ),
                priority=123,
                segment_version=123,
                tags=tags,
                template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                    email_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    )
                ),
                treatment_description="treatmentDescription",
                treatment_name="treatmentName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72587bc97db9489b7ff009b5e7e21b8672dd9834015792a5f49f1aa6e2de2b28)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument segment_id", value=segment_id, expected_type=type_hints["segment_id"])
            check_type(argname="argument additional_treatments", value=additional_treatments, expected_type=type_hints["additional_treatments"])
            check_type(argname="argument campaign_hook", value=campaign_hook, expected_type=type_hints["campaign_hook"])
            check_type(argname="argument custom_delivery_configuration", value=custom_delivery_configuration, expected_type=type_hints["custom_delivery_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument holdout_percent", value=holdout_percent, expected_type=type_hints["holdout_percent"])
            check_type(argname="argument is_paused", value=is_paused, expected_type=type_hints["is_paused"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument message_configuration", value=message_configuration, expected_type=type_hints["message_configuration"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument segment_version", value=segment_version, expected_type=type_hints["segment_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
            check_type(argname="argument treatment_description", value=treatment_description, expected_type=type_hints["treatment_description"])
            check_type(argname="argument treatment_name", value=treatment_name, expected_type=type_hints["treatment_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "name": name,
            "schedule": schedule,
            "segment_id": segment_id,
        }
        if additional_treatments is not None:
            self._values["additional_treatments"] = additional_treatments
        if campaign_hook is not None:
            self._values["campaign_hook"] = campaign_hook
        if custom_delivery_configuration is not None:
            self._values["custom_delivery_configuration"] = custom_delivery_configuration
        if description is not None:
            self._values["description"] = description
        if holdout_percent is not None:
            self._values["holdout_percent"] = holdout_percent
        if is_paused is not None:
            self._values["is_paused"] = is_paused
        if limits is not None:
            self._values["limits"] = limits
        if message_configuration is not None:
            self._values["message_configuration"] = message_configuration
        if priority is not None:
            self._values["priority"] = priority
        if segment_version is not None:
            self._values["segment_version"] = segment_version
        if tags is not None:
            self._values["tags"] = tags
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration
        if treatment_description is not None:
            self._values["treatment_description"] = treatment_description
        if treatment_name is not None:
            self._values["treatment_name"] = treatment_name

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the campaign is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.ScheduleProperty]:
        '''The schedule settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-schedule
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.ScheduleProperty], result)

    @builtins.property
    def segment_id(self) -> builtins.str:
        '''The unique identifier for the segment to associate with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentid
        '''
        result = self._values.get("segment_id")
        assert result is not None, "Required property 'segment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_treatments(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.WriteTreatmentResourceProperty]]]]:
        '''An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-additionaltreatments
        '''
        result = self._values.get("additional_treatments")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.WriteTreatmentResourceProperty]]]], result)

    @builtins.property
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.CampaignHookProperty]]:
        '''Specifies the Lambda function to use as a code hook for a campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-campaignhook
        '''
        result = self._values.get("campaign_hook")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.CampaignHookProperty]], result)

    @builtins.property
    def custom_delivery_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.CustomDeliveryConfigurationProperty]]:
        '''The delivery configuration settings for sending the treatment through a custom channel.

        This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-customdeliveryconfiguration
        '''
        result = self._values.get("custom_delivery_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.CustomDeliveryConfigurationProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def holdout_percent(self) -> typing.Optional[jsii.Number]:
        '''The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-holdoutpercent
        '''
        result = self._values.get("holdout_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to pause the campaign.

        A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-ispaused
        '''
        result = self._values.get("is_paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.LimitsProperty]]:
        '''The messaging limits for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-limits
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.LimitsProperty]], result)

    @builtins.property
    def message_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.MessageConfigurationProperty]]:
        '''The message configuration settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-messageconfiguration
        '''
        result = self._values.get("message_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.MessageConfigurationProperty]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest.

        If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def segment_version(self) -> typing.Optional[jsii.Number]:
        '''The version of the segment to associate with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentversion
        '''
        result = self._values.get("segment_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.TemplateConfigurationProperty]]:
        '''The message template to use for the treatment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-templateconfiguration
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.TemplateConfigurationProperty]], result)

    @builtins.property
    def treatment_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the default treatment for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentdescription
        '''
        result = self._values.get("treatment_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def treatment_name(self) -> typing.Optional[builtins.str]:
        '''A custom name of the default treatment for the campaign, if the campaign has multiple treatments.

        A *treatment* is a variation of a campaign that's used for A/B testing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentname
        '''
        result = self._values.get("treatment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCampaignProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEmailChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnEmailChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::EmailChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the email channel to send email to users. Before you can use Amazon Pinpoint to send email, you must enable the email channel for an Amazon Pinpoint application.

    The EmailChannel resource represents the status, identity, and other settings of the email channel for an application

    :cloudformationResource: AWS::Pinpoint::EmailChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_email_channel = pinpoint.CfnEmailChannel(self, "MyCfnEmailChannel",
            application_id="applicationId",
            from_address="fromAddress",
            identity="identity",
        
            # the properties below are optional
            configuration_set="configurationSet",
            enabled=False,
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        from_address: builtins.str,
        identity: builtins.str,
        configuration_set: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::EmailChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.
        :param from_address: The verified email address that you want to send email from when you send email through the channel.
        :param identity: The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.
        :param configuration_set: The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.
        :param enabled: Specifies whether to enable the email channel for the application.
        :param role_arn: The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45ef6803da11b29d92a1a9dedc966b47a1d2605b1fe5fccb5246dddfc35974a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEmailChannelProps(
            application_id=application_id,
            from_address=from_address,
            identity=identity,
            configuration_set=configuration_set,
            enabled=enabled,
            role_arn=role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba9980f2fd74da06e1ebc3614726e1c5828c881d5f32ab71fac8739256ea8c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3385e98cd386c8fd9b175addf07939f0a62ce826adf2dbbd5859a22437ec589)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4912ef26d0f430c81d117a5f0738e505c5c297269d1a30e2f2ebaadf888bc117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="fromAddress")
    def from_address(self) -> builtins.str:
        '''The verified email address that you want to send email from when you send email through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-fromaddress
        '''
        return typing.cast(builtins.str, jsii.get(self, "fromAddress"))

    @from_address.setter
    def from_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca335db0b8dfb92d4f3709cdefa228f99201c3be5f276ea0c1b91c43f2cfcf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromAddress", value)

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-identity
        '''
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @identity.setter
    def identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b0d7f51338958e8b630f2bab7314510884f2d03614c934c994658b597484a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value)

    @builtins.property
    @jsii.member(jsii_name="configurationSet")
    def configuration_set(self) -> typing.Optional[builtins.str]:
        '''The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-configurationset
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationSet"))

    @configuration_set.setter
    def configuration_set(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e401391c80933a2a367be2a6d52f36eece68b65d9cc1818ec569032f8db86e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSet", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the email channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5e325a8ba69d47d97054b07e5f37d86b62f5fc9a793b19194d843900f702ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec25179e4b582e0ac18ca6169a6cce37f50940251294b550528449a9abacbcfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnEmailChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "from_address": "fromAddress",
        "identity": "identity",
        "configuration_set": "configurationSet",
        "enabled": "enabled",
        "role_arn": "roleArn",
    },
)
class CfnEmailChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        from_address: builtins.str,
        identity: builtins.str,
        configuration_set: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEmailChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.
        :param from_address: The verified email address that you want to send email from when you send email through the channel.
        :param identity: The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.
        :param configuration_set: The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.
        :param enabled: Specifies whether to enable the email channel for the application.
        :param role_arn: The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_email_channel_props = pinpoint.CfnEmailChannelProps(
                application_id="applicationId",
                from_address="fromAddress",
                identity="identity",
            
                # the properties below are optional
                configuration_set="configurationSet",
                enabled=False,
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13cd2fd919777b8e7d3ac652f2b80d489a8fa271bc155e3f51e0609aec57178e)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument from_address", value=from_address, expected_type=type_hints["from_address"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument configuration_set", value=configuration_set, expected_type=type_hints["configuration_set"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "from_address": from_address,
            "identity": identity,
        }
        if configuration_set is not None:
            self._values["configuration_set"] = configuration_set
        if enabled is not None:
            self._values["enabled"] = enabled
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def from_address(self) -> builtins.str:
        '''The verified email address that you want to send email from when you send email through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-fromaddress
        '''
        result = self._values.get("from_address")
        assert result is not None, "Required property 'from_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-identity
        '''
        result = self._values.get("identity")
        assert result is not None, "Required property 'identity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_set(self) -> typing.Optional[builtins.str]:
        '''The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-configurationset
        '''
        result = self._values.get("configuration_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the email channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEmailTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnEmailTemplate",
):
    '''A CloudFormation ``AWS::Pinpoint::EmailTemplate``.

    Creates a message template that you can use in messages that are sent through the email channel. A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :cloudformationResource: AWS::Pinpoint::EmailTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        # tags: Any
        
        cfn_email_template = pinpoint.CfnEmailTemplate(self, "MyCfnEmailTemplate",
            subject="subject",
            template_name="templateName",
        
            # the properties below are optional
            default_substitutions="defaultSubstitutions",
            html_part="htmlPart",
            tags=tags,
            template_description="templateDescription",
            text_part="textPart"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        subject: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        html_part: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        text_part: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::EmailTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subject: The subject line, or title, to use in email messages that are based on the message template.
        :param template_name: The name of the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param html_part: The message body, in HTML format, to use in email messages that are based on the message template. We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        :param text_part: The message body, in plain text format, to use in email messages that are based on the message template. We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d874cd34a09cafe787407bcc46d4f2da25256379f0805d9b3277c78cf3a6ce7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEmailTemplateProps(
            subject=subject,
            template_name=template_name,
            default_substitutions=default_substitutions,
            html_part=html_part,
            tags=tags,
            template_description=template_description,
            text_part=text_part,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4845bb424606d811a5345c7d19273d48e2530fde2429a0b75c2de4451f2fe01d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46d26377f4991209d1040e8926b3268c77351920f64e91dcc7a8ee07bea65361)
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
        '''The Amazon Resource Name (ARN) of the message template.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        '''The subject line, or title, to use in email messages that are based on the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-subject
        '''
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ee602488855db74e55d0725ce9ccd5dcaf5afb7f9041fafb2a3f004cc023a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatename
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337414baf14212153d471a735df91b0b208b8e21f9a3af27ed8d45d4b33a256f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-defaultsubstitutions
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSubstitutions"))

    @default_substitutions.setter
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e725be82af784b9ad6a1f9c3380b3bd506f34418ddce549dec83efb2eda43c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property
    @jsii.member(jsii_name="htmlPart")
    def html_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in HTML format, to use in email messages that are based on the message template.

        We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-htmlpart
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlPart"))

    @html_part.setter
    def html_part(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96c5c7e2db544e6643fabe3a87b0849b9b5bfb84fd13605b99d18d53b8ec0ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlPart", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatedescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa0217316fb53d9c6411e9537d3910fb71d255ee4e4b5bf5a133a3388b54472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)

    @builtins.property
    @jsii.member(jsii_name="textPart")
    def text_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in plain text format, to use in email messages that are based on the message template.

        We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-textpart
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textPart"))

    @text_part.setter
    def text_part(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f43e87c31e4b4763bde93f0882c2fcaa98ebe283dee9aeb6c4de1c92a68b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textPart", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnEmailTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "subject": "subject",
        "template_name": "templateName",
        "default_substitutions": "defaultSubstitutions",
        "html_part": "htmlPart",
        "tags": "tags",
        "template_description": "templateDescription",
        "text_part": "textPart",
    },
)
class CfnEmailTemplateProps:
    def __init__(
        self,
        *,
        subject: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        html_part: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        text_part: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEmailTemplate``.

        :param subject: The subject line, or title, to use in email messages that are based on the message template.
        :param template_name: The name of the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param html_part: The message body, in HTML format, to use in email messages that are based on the message template. We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        :param text_part: The message body, in plain text format, to use in email messages that are based on the message template. We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            # tags: Any
            
            cfn_email_template_props = pinpoint.CfnEmailTemplateProps(
                subject="subject",
                template_name="templateName",
            
                # the properties below are optional
                default_substitutions="defaultSubstitutions",
                html_part="htmlPart",
                tags=tags,
                template_description="templateDescription",
                text_part="textPart"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ed26d7b8ff22bf96e4992ec66fa6f8f4f0a96e8dc7d62cfbe64407c8ad293a)
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument html_part", value=html_part, expected_type=type_hints["html_part"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
            check_type(argname="argument text_part", value=text_part, expected_type=type_hints["text_part"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject": subject,
            "template_name": template_name,
        }
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if html_part is not None:
            self._values["html_part"] = html_part
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description
        if text_part is not None:
            self._values["text_part"] = text_part

    @builtins.property
    def subject(self) -> builtins.str:
        '''The subject line, or title, to use in email messages that are based on the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-subject
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def html_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in HTML format, to use in email messages that are based on the message template.

        We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-htmlpart
        '''
        result = self._values.get("html_part")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in plain text format, to use in email messages that are based on the message template.

        We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-textpart
        '''
        result = self._values.get("text_part")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEventStream(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnEventStream",
):
    '''A CloudFormation ``AWS::Pinpoint::EventStream``.

    Creates a new event stream for an application or updates the settings of an existing event stream for an application.

    :cloudformationResource: AWS::Pinpoint::EventStream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_event_stream = pinpoint.CfnEventStream(self, "MyCfnEventStream",
            application_id="applicationId",
            destination_stream_arn="destinationStreamArn",
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        destination_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::EventStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you want to export data from.
        :param destination_stream_arn: The Amazon Resource Name (ARN) of the Amazon Kinesis data stream or Amazon Kinesis Data Firehose delivery stream that you want to publish event data to. For a Kinesis data stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name`` For a Kinesis Data Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``
        :param role_arn: The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be03b3b08c645b2ad088545ed60becc2d502a22d37e02777bb921d0c4359349)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEventStreamProps(
            application_id=application_id,
            destination_stream_arn=destination_stream_arn,
            role_arn=role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8094e769a5b01a2b647af323a98530df95848e983909ad98fd70769294a342eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65223bde3aa70f7290d5d29057c7fc736f1f73560d2ff8478c0c1e4dfc5e999e)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you want to export data from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b72a36d4dbe0f60f071d9d942bfb6de4e856a7c430f57175604abaef6219a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="destinationStreamArn")
    def destination_stream_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Kinesis data stream or Amazon Kinesis Data Firehose delivery stream that you want to publish event data to.

        For a Kinesis data stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name``

        For a Kinesis Data Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-destinationstreamarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationStreamArn"))

    @destination_stream_arn.setter
    def destination_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b623a340671fc74c6884cc8202757c872bd3257d4604b29a217712eae288de90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationStreamArn", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc07fa45109777e615e00fbd7316434ce79f2ac50097d2ac51d5d666ae068c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnEventStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "destination_stream_arn": "destinationStreamArn",
        "role_arn": "roleArn",
    },
)
class CfnEventStreamProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        destination_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnEventStream``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that you want to export data from.
        :param destination_stream_arn: The Amazon Resource Name (ARN) of the Amazon Kinesis data stream or Amazon Kinesis Data Firehose delivery stream that you want to publish event data to. For a Kinesis data stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name`` For a Kinesis Data Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``
        :param role_arn: The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_event_stream_props = pinpoint.CfnEventStreamProps(
                application_id="applicationId",
                destination_stream_arn="destinationStreamArn",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdb6b683e1b3c8b0ac5e4a9cbb95477d4817191bf0ad969320e26b97ee46b06)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument destination_stream_arn", value=destination_stream_arn, expected_type=type_hints["destination_stream_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "destination_stream_arn": destination_stream_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you want to export data from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_stream_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Kinesis data stream or Amazon Kinesis Data Firehose delivery stream that you want to publish event data to.

        For a Kinesis data stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name``

        For a Kinesis Data Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-destinationstreamarn
        '''
        result = self._values.get("destination_stream_arn")
        assert result is not None, "Required property 'destination_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGCMChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnGCMChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::GCMChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the GCM channel to send push notification messages to the Firebase Cloud Messaging (FCM) service, which replaced the Google Cloud Messaging (GCM) service. Before you use Amazon Pinpoint to send notifications to FCM, you have to enable the GCM channel for an Amazon Pinpoint application.

    The GCMChannel resource represents the status and authentication settings of the GCM channel for an application.

    :cloudformationResource: AWS::Pinpoint::GCMChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_gCMChannel = pinpoint.CfnGCMChannel(self, "MyCfnGCMChannel",
            api_key="apiKey",
            application_id="applicationId",
        
            # the properties below are optional
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::GCMChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key: The Web API key, also called the *server key* , that you received from Google to communicate with Google services.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.
        :param enabled: Specifies whether to enable the GCM channel for the Amazon Pinpoint application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9eaed45ea8e982f4384e74c9bb6d58e2bb50ab71b81ec8eb9663834eb40f68)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGCMChannelProps(
            api_key=api_key, application_id=application_id, enabled=enabled
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee2520c4272e766ba0a4239c563996907ec8d82983b8607a06d8c97c3f54f2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b8a9d9b2d9710aff98ca425ef3c722efadd68d8f9375e71c4e53100ed902c60)
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
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        '''The Web API key, also called the *server key* , that you received from Google to communicate with Google services.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-apikey
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe18164e431a229dfe4f3ed6e8be1938713396f5bc4716314cb650fc5c2ae14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value)

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ffd241afdcfa2aaf15677fee87435e32a5181cbbc3c5c41110b35f6e8fadbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the GCM channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307c8de02e27724c405c014f9dd6a91edb3c2ccf9dd15c311a610f1fd53b97f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnGCMChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_id": "applicationId",
        "enabled": "enabled",
    },
)
class CfnGCMChannelProps:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGCMChannel``.

        :param api_key: The Web API key, also called the *server key* , that you received from Google to communicate with Google services.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.
        :param enabled: Specifies whether to enable the GCM channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_gCMChannel_props = pinpoint.CfnGCMChannelProps(
                api_key="apiKey",
                application_id="applicationId",
            
                # the properties below are optional
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799575c91c7b790ecebe50a1f908591fa3d7d3754d560c5f8051e43307513e57)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def api_key(self) -> builtins.str:
        '''The Web API key, also called the *server key* , that you received from Google to communicate with Google services.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-apikey
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the GCM channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGCMChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnInAppTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnInAppTemplate",
):
    '''A CloudFormation ``AWS::Pinpoint::InAppTemplate``.

    Creates a message template that you can use to send in-app messages. A message template is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :cloudformationResource: AWS::Pinpoint::InAppTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        # custom_config: Any
        # tags: Any
        
        cfn_in_app_template = pinpoint.CfnInAppTemplate(self, "MyCfnInAppTemplate",
            template_name="templateName",
        
            # the properties below are optional
            content=[pinpoint.CfnInAppTemplate.InAppMessageContentProperty(
                background_color="backgroundColor",
                body_config=pinpoint.CfnInAppTemplate.BodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                ),
                header_config=pinpoint.CfnInAppTemplate.HeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                ),
                image_url="imageUrl",
                primary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                    android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                ),
                secondary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                    android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            )],
            custom_config=custom_config,
            layout="layout",
            tags=tags,
            template_description="templateDescription"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        template_name: builtins.str,
        content: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.InAppMessageContentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        custom_config: typing.Any = None,
        layout: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::InAppTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_name: The name of the in-app message template.
        :param content: An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.
        :param custom_config: Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.
        :param layout: A string that determines the appearance of the in-app message. You can specify one of the following:. - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page. - ``TOP_BANNER`` – a message that appears as a banner at the top of the page. - ``OVERLAYS`` – a message that covers entire screen. - ``MOBILE_FEED`` – a message that appears in a window in front of the page. - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page. - ``CAROUSEL`` – a scrollable layout of up to five unique messages.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: An optional description of the in-app template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a58375e3084247c0cd1a4551d9a749b021dbad12e66dc0d65d7097eeb389a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInAppTemplateProps(
            template_name=template_name,
            content=content,
            custom_config=custom_config,
            layout=layout,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa623197ed8dfdd5b6ea077a1267564e38ed76cde7a3f481fcda475c5fd3b44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee4100f78394daa226aff89f00d55dec1b35182e9d1582823bf3a6c1684ec5f2)
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
        '''The Amazon Resource Name (ARN) of the message template.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="customConfig")
    def custom_config(self) -> typing.Any:
        '''Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-customconfig
        '''
        return typing.cast(typing.Any, jsii.get(self, "customConfig"))

    @custom_config.setter
    def custom_config(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0f5b30324249dbcf7967883532e48ac34155fc6a825e970ce7caa894e09229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customConfig", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the in-app message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatename
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c54c1db617edfaec2d1880df4f13dd162442c1cad515fa6ada8b050e5cdf50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.InAppMessageContentProperty"]]]]:
        '''An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-content
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.InAppMessageContentProperty"]]]], jsii.get(self, "content"))

    @content.setter
    def content(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.InAppMessageContentProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278ac4934402735235bea728305420ef61f4374ceca39785b68d3ab9024dd011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="layout")
    def layout(self) -> typing.Optional[builtins.str]:
        '''A string that determines the appearance of the in-app message. You can specify one of the following:.

        - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page.
        - ``TOP_BANNER`` – a message that appears as a banner at the top of the page.
        - ``OVERLAYS`` – a message that covers entire screen.
        - ``MOBILE_FEED`` – a message that appears in a window in front of the page.
        - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page.
        - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-layout
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "layout"))

    @layout.setter
    def layout(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd98e575ebe4e3646735d441e76df71a700ae5750834bd3fe9efea0bb3f8d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layout", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the in-app template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatedescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea20c5d2a069fd71769a2945612fa3a4466fef3a6c3ca5d82dbc959098901f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnInAppTemplate.BodyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "body": "body",
            "text_color": "textColor",
        },
    )
    class BodyConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of the main body text of the in-app message.

            :param alignment: The text alignment of the main body text of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param body: The main body text of the message.
            :param text_color: The color of the body text, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                body_config_property = pinpoint.CfnInAppTemplate.BodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d89b51b3c0403b7d96e89a3d4ddd4537a1fa88688411aaf0eaf90733bcf98e0)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if body is not None:
                self._values["body"] = body
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the main body text of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The main body text of the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BodyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnInAppTemplate.ButtonConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "android": "android",
            "default_config": "defaultConfig",
            "ios": "ios",
            "web": "web",
        },
    )
    class ButtonConfigProperty:
        def __init__(
            self,
            *,
            android: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.DefaultButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ios: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            web: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the behavior of buttons that appear in an in-app message template.

            :param android: Optional button configuration to use for in-app messages sent to Android devices. This button configuration overrides the default button configuration.
            :param default_config: Specifies the default behavior of a button that appears in an in-app message. You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.
            :param ios: Optional button configuration to use for in-app messages sent to iOS devices. This button configuration overrides the default button configuration.
            :param web: Optional button configuration to use for in-app messages sent to web applications. This button configuration overrides the default button configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                button_config_property = pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                    android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8bfbd704c6147b782ea69635d057627ac5ca2b9a14e9ed9df555a39a159d97c9)
                check_type(argname="argument android", value=android, expected_type=type_hints["android"])
                check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
                check_type(argname="argument ios", value=ios, expected_type=type_hints["ios"])
                check_type(argname="argument web", value=web, expected_type=type_hints["web"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if android is not None:
                self._values["android"] = android
            if default_config is not None:
                self._values["default_config"] = default_config
            if ios is not None:
                self._values["ios"] = ios
            if web is not None:
                self._values["web"] = web

        @builtins.property
        def android(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.OverrideButtonConfigurationProperty"]]:
            '''Optional button configuration to use for in-app messages sent to Android devices.

            This button configuration overrides the default button configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-android
            '''
            result = self._values.get("android")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.OverrideButtonConfigurationProperty"]], result)

        @builtins.property
        def default_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.DefaultButtonConfigurationProperty"]]:
            '''Specifies the default behavior of a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-defaultconfig
            '''
            result = self._values.get("default_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.DefaultButtonConfigurationProperty"]], result)

        @builtins.property
        def ios(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.OverrideButtonConfigurationProperty"]]:
            '''Optional button configuration to use for in-app messages sent to iOS devices.

            This button configuration overrides the default button configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-ios
            '''
            result = self._values.get("ios")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.OverrideButtonConfigurationProperty"]], result)

        @builtins.property
        def web(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.OverrideButtonConfigurationProperty"]]:
            '''Optional button configuration to use for in-app messages sent to web applications.

            This button configuration overrides the default button configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-web
            '''
            result = self._values.get("web")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.OverrideButtonConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ButtonConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "border_radius": "borderRadius",
            "button_action": "buttonAction",
            "link": "link",
            "text": "text",
            "text_color": "textColor",
        },
    )
    class DefaultButtonConfigurationProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            border_radius: typing.Optional[jsii.Number] = None,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
            text: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default behavior of a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :param background_color: The background color of a button, expressed as a hex color code (such as #000000 for black).
            :param border_radius: The border radius of a button.
            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.
            :param text: The text that appears on a button in an in-app message.
            :param text_color: The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                default_button_configuration_property = pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                    background_color="backgroundColor",
                    border_radius=123,
                    button_action="buttonAction",
                    link="link",
                    text="text",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abf7eb85b29234b3c2fea6fe8ac046f242a6f8637d3e8cb84baf14ee553046c0)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument border_radius", value=border_radius, expected_type=type_hints["border_radius"])
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if border_radius is not None:
                self._values["border_radius"] = border_radius
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link
            if text is not None:
                self._values["text"] = text
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color of a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def border_radius(self) -> typing.Optional[jsii.Number]:
            '''The border radius of a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-borderradius
            '''
            result = self._values.get("border_radius")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text that appears on a button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnInAppTemplate.HeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "header": "header",
            "text_color": "textColor",
        },
    )
    class HeaderConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            header: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :param alignment: The text alignment of the title of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param header: The title text of the in-app message.
            :param text_color: The color of the title text, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                header_config_property = pinpoint.CfnInAppTemplate.HeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc7d7f00dba390851da4a74e15f2cbfba584ff0c3dcfd02c79057d3e495a8426)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if header is not None:
                self._values["header"] = header
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the title of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header(self) -> typing.Optional[builtins.str]:
            '''The title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-header
            '''
            result = self._values.get("header")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the title text, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnInAppTemplate.InAppMessageContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "body_config": "bodyConfig",
            "header_config": "headerConfig",
            "image_url": "imageUrl",
            "primary_btn": "primaryBtn",
            "secondary_btn": "secondaryBtn",
        },
    )
    class InAppMessageContentProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            body_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.BodyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            header_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.HeaderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_url: typing.Optional[builtins.str] = None,
            primary_btn: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.ButtonConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secondary_btn: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInAppTemplate.ButtonConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration of an in-app message, including its header, body, buttons, colors, and images.

            :param background_color: The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).
            :param body_config: An object that contains configuration information about the header or title text of the in-app message.
            :param header_config: An object that contains configuration information about the header or title text of the in-app message.
            :param image_url: The URL of the image that appears on an in-app message banner.
            :param primary_btn: An object that contains configuration information about the primary button in an in-app message.
            :param secondary_btn: An object that contains configuration information about the secondary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                in_app_message_content_property = pinpoint.CfnInAppTemplate.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint.CfnInAppTemplate.BodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint.CfnInAppTemplate.HeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                        android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                        android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86ad4b85282ac1d2a8384b4d73f0ea53928263965bc0416ac9676a6e6dc68ab6)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument body_config", value=body_config, expected_type=type_hints["body_config"])
                check_type(argname="argument header_config", value=header_config, expected_type=type_hints["header_config"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument primary_btn", value=primary_btn, expected_type=type_hints["primary_btn"])
                check_type(argname="argument secondary_btn", value=secondary_btn, expected_type=type_hints["secondary_btn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if body_config is not None:
                self._values["body_config"] = body_config
            if header_config is not None:
                self._values["header_config"] = header_config
            if image_url is not None:
                self._values["image_url"] = image_url
            if primary_btn is not None:
                self._values["primary_btn"] = primary_btn
            if secondary_btn is not None:
                self._values["secondary_btn"] = secondary_btn

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.BodyConfigProperty"]]:
            '''An object that contains configuration information about the header or title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-bodyconfig
            '''
            result = self._values.get("body_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.BodyConfigProperty"]], result)

        @builtins.property
        def header_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.HeaderConfigProperty"]]:
            '''An object that contains configuration information about the header or title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-headerconfig
            '''
            result = self._values.get("header_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.HeaderConfigProperty"]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image that appears on an in-app message banner.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_btn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.ButtonConfigProperty"]]:
            '''An object that contains configuration information about the primary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-primarybtn
            '''
            result = self._values.get("primary_btn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.ButtonConfigProperty"]], result)

        @builtins.property
        def secondary_btn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.ButtonConfigProperty"]]:
            '''An object that contains configuration information about the secondary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-secondarybtn
            '''
            result = self._values.get("secondary_btn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInAppTemplate.ButtonConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"button_action": "buttonAction", "link": "link"},
    )
    class OverrideButtonConfigurationProperty:
        def __init__(
            self,
            *,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of a button with settings that are specific to a certain device type.

            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                override_button_configuration_property = pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                    button_action="buttonAction",
                    link="link"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07dcbc742cada193c5c4b997d8176916ddf68dcc52fd8cb5f229362873c40ec4)
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html#cfn-pinpoint-inapptemplate-overridebuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html#cfn-pinpoint-inapptemplate-overridebuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnInAppTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_name": "templateName",
        "content": "content",
        "custom_config": "customConfig",
        "layout": "layout",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnInAppTemplateProps:
    def __init__(
        self,
        *,
        template_name: builtins.str,
        content: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        custom_config: typing.Any = None,
        layout: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnInAppTemplate``.

        :param template_name: The name of the in-app message template.
        :param content: An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.
        :param custom_config: Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.
        :param layout: A string that determines the appearance of the in-app message. You can specify one of the following:. - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page. - ``TOP_BANNER`` – a message that appears as a banner at the top of the page. - ``OVERLAYS`` – a message that covers entire screen. - ``MOBILE_FEED`` – a message that appears in a window in front of the page. - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page. - ``CAROUSEL`` – a scrollable layout of up to five unique messages.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: An optional description of the in-app template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            # custom_config: Any
            # tags: Any
            
            cfn_in_app_template_props = pinpoint.CfnInAppTemplateProps(
                template_name="templateName",
            
                # the properties below are optional
                content=[pinpoint.CfnInAppTemplate.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint.CfnInAppTemplate.BodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint.CfnInAppTemplate.HeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                        android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                        android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )],
                custom_config=custom_config,
                layout="layout",
                tags=tags,
                template_description="templateDescription"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d93034b4533bd842d7be555c9eef0012056db058958d6e0180cd8b62e90620b)
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
            check_type(argname="argument layout", value=layout, expected_type=type_hints["layout"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_name": template_name,
        }
        if content is not None:
            self._values["content"] = content
        if custom_config is not None:
            self._values["custom_config"] = custom_config
        if layout is not None:
            self._values["layout"] = layout
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the in-app message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInAppTemplate.InAppMessageContentProperty]]]]:
        '''An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInAppTemplate.InAppMessageContentProperty]]]], result)

    @builtins.property
    def custom_config(self) -> typing.Any:
        '''Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-customconfig
        '''
        result = self._values.get("custom_config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def layout(self) -> typing.Optional[builtins.str]:
        '''A string that determines the appearance of the in-app message. You can specify one of the following:.

        - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page.
        - ``TOP_BANNER`` – a message that appears as a banner at the top of the page.
        - ``OVERLAYS`` – a message that covers entire screen.
        - ``MOBILE_FEED`` – a message that appears in a window in front of the page.
        - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page.
        - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-layout
        '''
        result = self._values.get("layout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the in-app template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInAppTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPushTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnPushTemplate",
):
    '''A CloudFormation ``AWS::Pinpoint::PushTemplate``.

    Creates a message template that you can use in messages that are sent through a push notification channel. A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :cloudformationResource: AWS::Pinpoint::PushTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        # tags: Any
        
        cfn_push_template = pinpoint.CfnPushTemplate(self, "MyCfnPushTemplate",
            template_name="templateName",
        
            # the properties below are optional
            adm=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            apns=pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty(
                action="action",
                body="body",
                media_url="mediaUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            baidu=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            default=pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty(
                action="action",
                body="body",
                sound="sound",
                title="title",
                url="url"
            ),
            default_substitutions="defaultSubstitutions",
            gcm=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            tags=tags,
            template_description="templateDescription"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        template_name: builtins.str,
        adm: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        apns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPushTemplate.APNSPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        baidu: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPushTemplate.DefaultPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_substitutions: typing.Optional[builtins.str] = None,
        gcm: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::PushTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_name: The name of the message template.
        :param adm: The message template to use for the ADM (Amazon Device Messaging) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param apns: The message template to use for the APNs (Apple Push Notification service) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param baidu: The message template to use for the Baidu (Baidu Cloud Push) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param default: The default message template to use for push notification channels.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param gcm: The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e234330089d446d7f323e4c73f1d9c1c17acc0e0e30d28c97d54c37c7c4a76e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPushTemplateProps(
            template_name=template_name,
            adm=adm,
            apns=apns,
            baidu=baidu,
            default=default,
            default_substitutions=default_substitutions,
            gcm=gcm,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69fca92e478053d0cc44916fbd64e74a2cb6e71987f1f78cd6f6dc1d560f3c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1368e70eaee432841f8a64dd25110474cab976d2646e829941e7dd0026b49aaf)
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
        '''The Amazon Resource Name (ARN) of the message template.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatename
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733a68483e3bb9f727ebd95cdd0c0c723459549bfff847d29285135a1dc73c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="adm")
    def adm(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]]:
        '''The message template to use for the ADM (Amazon Device Messaging) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-adm
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]], jsii.get(self, "adm"))

    @adm.setter
    def adm(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3e0bfcf687191128b7b58605ea3ecd33d73aeee2ce7892a26c98f627ddba49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adm", value)

    @builtins.property
    @jsii.member(jsii_name="apns")
    def apns(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.APNSPushNotificationTemplateProperty"]]:
        '''The message template to use for the APNs (Apple Push Notification service) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-apns
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.APNSPushNotificationTemplateProperty"]], jsii.get(self, "apns"))

    @apns.setter
    def apns(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.APNSPushNotificationTemplateProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e2be7f43670056e7a6d731558fa33e8cf4475c8540b11898df56b3140d9ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apns", value)

    @builtins.property
    @jsii.member(jsii_name="baidu")
    def baidu(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]]:
        '''The message template to use for the Baidu (Baidu Cloud Push) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-baidu
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]], jsii.get(self, "baidu"))

    @baidu.setter
    def baidu(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169b7f0cdb9b4fd53c5a7349f078aff8f1b19f6fad401e78c6e0669fa2a1b01c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baidu", value)

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.DefaultPushNotificationTemplateProperty"]]:
        '''The default message template to use for push notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-default
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.DefaultPushNotificationTemplateProperty"]], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.DefaultPushNotificationTemplateProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520329f747f3fe8b8d0fd51174dae9ab0a39a0f6cbe587a14b80cad8f1d3a871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-defaultsubstitutions
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSubstitutions"))

    @default_substitutions.setter
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267ffcf4c6fca6192a102836f31a68c1a2ef0fc2b356b8df2374ba24a679ac76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property
    @jsii.member(jsii_name="gcm")
    def gcm(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]]:
        '''The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-gcm
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]], jsii.get(self, "gcm"))

    @gcm.setter
    def gcm(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPushTemplate.AndroidPushNotificationTemplateProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878bb27810504a86ab7ea470a0e25a1c91ca228c671844b097b4ba0125c444d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcm", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatedescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7291a982a472e0124687c43898c55ff61676c9c406522250462b9c8a234efb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "media_url": "mediaUrl",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class APNSPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            media_url: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies channel-specific content and settings for a message template that can be used in push notifications that are sent through the APNs (Apple Push Notification service) channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS platform. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in push notifications that are based on the message template.
            :param media_url: The URL of an image or video to display in push notifications that are based on the message template.
            :param sound: The key for the sound to play when the recipient receives a push notification that's based on the message template. The value for this key is the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.
            :param title: The title to use in push notifications that are based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in the recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                a_pNSPush_notification_template_property = pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    media_url="mediaUrl",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5eb0a399816d80399f7992f464408e5a015c38f3887194c0a8ec7fc67e726678)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument media_url", value=media_url, expected_type=type_hints["media_url"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if media_url is not None:
                self._values["media_url"] = media_url
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS platform.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in push notifications that are based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def media_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image or video to display in push notifications that are based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-mediaurl
            '''
            result = self._values.get("media_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The key for the sound to play when the recipient receives a push notification that's based on the message template.

            The value for this key is the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in push notifications that are based on the message template.

            This title appears above the notification message on a recipient's device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in the recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "APNSPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "image_icon_url": "imageIconUrl",
            "image_url": "imageUrl",
            "small_image_icon_url": "smallImageIconUrl",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class AndroidPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            image_icon_url: typing.Optional[builtins.str] = None,
            image_url: typing.Optional[builtins.str] = None,
            small_image_icon_url: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies channel-specific content and settings for a message template that can be used in push notifications that are sent through the ADM (Amazon Device Messaging), Baidu (Baidu Cloud Push), or GCM (Firebase Cloud Messaging, formerly Google Cloud Messaging) channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This action uses the deep-linking features of the Android platform. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in a push notification that's based on the message template.
            :param image_icon_url: The URL of the large icon image to display in the content view of a push notification that's based on the message template.
            :param image_url: The URL of an image to display in a push notification that's based on the message template.
            :param small_image_icon_url: The URL of the small icon image to display in the status bar and the content view of a push notification that's based on the message template.
            :param sound: The sound to play when a recipient receives a push notification that's based on the message template. You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .
            :param title: The title to use in a push notification that's based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                android_push_notification_template_property = pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f866be8e13a626d05404b7f7c753cce31f96ee49c91fb4e9328cd1e1ff25e66)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument image_icon_url", value=image_icon_url, expected_type=type_hints["image_icon_url"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument small_image_icon_url", value=small_image_icon_url, expected_type=type_hints["small_image_icon_url"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if image_icon_url is not None:
                self._values["image_icon_url"] = image_icon_url
            if image_url is not None:
                self._values["image_url"] = image_url
            if small_image_icon_url is not None:
                self._values["small_image_icon_url"] = small_image_icon_url
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This action uses the deep-linking features of the Android platform.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in a push notification that's based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the large icon image to display in the content view of a push notification that's based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-imageiconurl
            '''
            result = self._values.get("image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image to display in a push notification that's based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def small_image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the small icon image to display in the status bar and the content view of a push notification that's based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-smallimageiconurl
            '''
            result = self._values.get("small_image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The sound to play when a recipient receives a push notification that's based on the message template.

            You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in a push notification that's based on the message template.

            This title appears above the notification message on a recipient's device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndroidPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class DefaultPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default settings and content for a message template that can be used in messages that are sent through a push notification channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS and Android platforms. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in push notifications that are based on the message template.
            :param sound: The sound to play when a recipient receives a push notification that's based on the message template. You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` . For an iOS platform, this value is the key for the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.
            :param title: The title to use in push notifications that are based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                default_push_notification_template_property = pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5c71269ade76af4dae966ba08f6aa0718ac78505a335761ef4f79a8955a35fa)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS and Android platforms.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in push notifications that are based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The sound to play when a recipient receives a push notification that's based on the message template.

            You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .

            For an iOS platform, this value is the key for the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in push notifications that are based on the message template.

            This title appears above the notification message on a recipient's device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnPushTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_name": "templateName",
        "adm": "adm",
        "apns": "apns",
        "baidu": "baidu",
        "default": "default",
        "default_substitutions": "defaultSubstitutions",
        "gcm": "gcm",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnPushTemplateProps:
    def __init__(
        self,
        *,
        template_name: builtins.str,
        adm: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        apns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        baidu: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        default: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_substitutions: typing.Optional[builtins.str] = None,
        gcm: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPushTemplate``.

        :param template_name: The name of the message template.
        :param adm: The message template to use for the ADM (Amazon Device Messaging) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param apns: The message template to use for the APNs (Apple Push Notification service) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param baidu: The message template to use for the Baidu (Baidu Cloud Push) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param default: The default message template to use for push notification channels.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param gcm: The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            # tags: Any
            
            cfn_push_template_props = pinpoint.CfnPushTemplateProps(
                template_name="templateName",
            
                # the properties below are optional
                adm=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                apns=pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    media_url="mediaUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                baidu=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                default=pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                default_substitutions="defaultSubstitutions",
                gcm=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                tags=tags,
                template_description="templateDescription"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444f4f10de75d3627ca6a158b3d14a85658b8f8d43cf6e0ff75307e722782866)
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument adm", value=adm, expected_type=type_hints["adm"])
            check_type(argname="argument apns", value=apns, expected_type=type_hints["apns"])
            check_type(argname="argument baidu", value=baidu, expected_type=type_hints["baidu"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument gcm", value=gcm, expected_type=type_hints["gcm"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_name": template_name,
        }
        if adm is not None:
            self._values["adm"] = adm
        if apns is not None:
            self._values["apns"] = apns
        if baidu is not None:
            self._values["baidu"] = baidu
        if default is not None:
            self._values["default"] = default
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if gcm is not None:
            self._values["gcm"] = gcm
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def adm(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]]:
        '''The message template to use for the ADM (Amazon Device Messaging) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-adm
        '''
        result = self._values.get("adm")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]], result)

    @builtins.property
    def apns(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.APNSPushNotificationTemplateProperty]]:
        '''The message template to use for the APNs (Apple Push Notification service) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-apns
        '''
        result = self._values.get("apns")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.APNSPushNotificationTemplateProperty]], result)

    @builtins.property
    def baidu(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]]:
        '''The message template to use for the Baidu (Baidu Cloud Push) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-baidu
        '''
        result = self._values.get("baidu")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]], result)

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.DefaultPushNotificationTemplateProperty]]:
        '''The default message template to use for push notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-default
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.DefaultPushNotificationTemplateProperty]], result)

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcm(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]]:
        '''The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-gcm
        '''
        result = self._values.get("gcm")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPushTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSMSChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnSMSChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::SMSChannel``.

    A *channel* is a type of platform that you can deliver messages to. To send an SMS text message, you send the message through the SMS channel. Before you can use Amazon Pinpoint to send text messages, you have to enable the SMS channel for an Amazon Pinpoint application.

    The SMSChannel resource represents the status, sender ID, and other settings for the SMS channel for an application.

    :cloudformationResource: AWS::Pinpoint::SMSChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_sMSChannel = pinpoint.CfnSMSChannel(self, "MyCfnSMSChannel",
            application_id="applicationId",
        
            # the properties below are optional
            enabled=False,
            sender_id="senderId",
            short_code="shortCode"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        sender_id: typing.Optional[builtins.str] = None,
        short_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::SMSChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.
        :param enabled: Specifies whether to enable the SMS channel for the application.
        :param sender_id: The identity that you want to display on recipients' devices when they receive messages from the SMS channel. .. epigraph:: SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .
        :param short_code: The registered short code that you want to use when you send messages through the SMS channel. .. epigraph:: For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247e0e5db6df3760ce5285f312696c0525a8122dab3a894fc9e420f45b608f5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSMSChannelProps(
            application_id=application_id,
            enabled=enabled,
            sender_id=sender_id,
            short_code=short_code,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5eddd6bebc84e2365315fd2909a8d2a359e9c879be4ad3b8fb696c82861e9ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1499f7e636fe54076eb88578edbc4d2d332ca41d00d40e34d42ae56c780783cb)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979edcd25a20504bee120865d3c675d946146871879017a777fb6466da3cc52e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the SMS channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690b91b19b5fb26df4cd2a5740ffa6004a6a6f66aad08a1dd7cea96e210cd237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="senderId")
    def sender_id(self) -> typing.Optional[builtins.str]:
        '''The identity that you want to display on recipients' devices when they receive messages from the SMS channel.

        .. epigraph::

           SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-senderid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "senderId"))

    @sender_id.setter
    def sender_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a965e648aedad26bca950f0ef0214b33d05f0acd6812182eb6b2f4c0cf2896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "senderId", value)

    @builtins.property
    @jsii.member(jsii_name="shortCode")
    def short_code(self) -> typing.Optional[builtins.str]:
        '''The registered short code that you want to use when you send messages through the SMS channel.

        .. epigraph::

           For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-shortcode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shortCode"))

    @short_code.setter
    def short_code(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd359def565ce7c57596d41d3957b09dfa4a8d5b03403b031c18e654739247c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shortCode", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnSMSChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "enabled": "enabled",
        "sender_id": "senderId",
        "short_code": "shortCode",
    },
)
class CfnSMSChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        sender_id: typing.Optional[builtins.str] = None,
        short_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSMSChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.
        :param enabled: Specifies whether to enable the SMS channel for the application.
        :param sender_id: The identity that you want to display on recipients' devices when they receive messages from the SMS channel. .. epigraph:: SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .
        :param short_code: The registered short code that you want to use when you send messages through the SMS channel. .. epigraph:: For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_sMSChannel_props = pinpoint.CfnSMSChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                enabled=False,
                sender_id="senderId",
                short_code="shortCode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931b6acba9303ee19a2283bc8a621a4eefb65d2b2880b2ef0ffbb1467a2996eb)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument sender_id", value=sender_id, expected_type=type_hints["sender_id"])
            check_type(argname="argument short_code", value=short_code, expected_type=type_hints["short_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if sender_id is not None:
            self._values["sender_id"] = sender_id
        if short_code is not None:
            self._values["short_code"] = short_code

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the SMS channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def sender_id(self) -> typing.Optional[builtins.str]:
        '''The identity that you want to display on recipients' devices when they receive messages from the SMS channel.

        .. epigraph::

           SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-senderid
        '''
        result = self._values.get("sender_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def short_code(self) -> typing.Optional[builtins.str]:
        '''The registered short code that you want to use when you send messages through the SMS channel.

        .. epigraph::

           For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-shortcode
        '''
        result = self._values.get("short_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSMSChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSegment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnSegment",
):
    '''A CloudFormation ``AWS::Pinpoint::Segment``.

    Updates the configuration, dimension, and other settings for an existing segment.

    :cloudformationResource: AWS::Pinpoint::Segment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        # attributes: Any
        # metrics: Any
        # tags: Any
        # user_attributes: Any
        
        cfn_segment = pinpoint.CfnSegment(self, "MyCfnSegment",
            application_id="applicationId",
            name="name",
        
            # the properties below are optional
            dimensions=pinpoint.CfnSegment.SegmentDimensionsProperty(
                attributes=attributes,
                behavior=pinpoint.CfnSegment.BehaviorProperty(
                    recency=pinpoint.CfnSegment.RecencyProperty(
                        duration="duration",
                        recency_type="recencyType"
                    )
                ),
                demographic=pinpoint.CfnSegment.DemographicProperty(
                    app_version=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    channel=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    device_type=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    make=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    model=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    platform=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    )
                ),
                location=pinpoint.CfnSegment.LocationProperty(
                    country=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    gps_point=pinpoint.CfnSegment.GPSPointProperty(
                        coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                            latitude=123,
                            longitude=123
                        ),
                        range_in_kilometers=123
                    )
                ),
                metrics=metrics,
                user_attributes=user_attributes
            ),
            segment_groups=pinpoint.CfnSegment.SegmentGroupsProperty(
                groups=[pinpoint.CfnSegment.GroupsProperty(
                    dimensions=[pinpoint.CfnSegment.SegmentDimensionsProperty(
                        attributes=attributes,
                        behavior=pinpoint.CfnSegment.BehaviorProperty(
                            recency=pinpoint.CfnSegment.RecencyProperty(
                                duration="duration",
                                recency_type="recencyType"
                            )
                        ),
                        demographic=pinpoint.CfnSegment.DemographicProperty(
                            app_version=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            channel=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            device_type=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            make=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            model=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            platform=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        location=pinpoint.CfnSegment.LocationProperty(
                            country=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            gps_point=pinpoint.CfnSegment.GPSPointProperty(
                                coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                    latitude=123,
                                    longitude=123
                                ),
                                range_in_kilometers=123
                            )
                        ),
                        metrics=metrics,
                        user_attributes=user_attributes
                    )],
                    source_segments=[pinpoint.CfnSegment.SourceSegmentsProperty(
                        id="id",
        
                        # the properties below are optional
                        version=123
                    )],
                    source_type="sourceType",
                    type="type"
                )],
                include="include"
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        name: builtins.str,
        dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SegmentDimensionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        segment_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SegmentGroupsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::Segment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the segment is associated with.
        :param name: The name of the segment.
        :param dimensions: The criteria that define the dimensions for the segment.
        :param segment_groups: The segment group to use and the dimensions to apply to the group's base segments in order to build the segment. A segment group can consist of zero or more base segments. Your request can include only one segment group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc023e804159f2b7b3b0630adc967114ee69038688e93e460806bebbcd49abd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSegmentProps(
            application_id=application_id,
            name=name,
            dimensions=dimensions,
            segment_groups=segment_groups,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7365726c90040db7625826a2214e0e44dc196900ff6edeb46c088ea26bbca5a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f392d88b193fdce847c6174f5ce8112cca1b45b84d5109a4b4c63735f9cd9e4b)
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
        '''The Amazon Resource Name (ARN) of the segment.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSegmentId")
    def attr_segment_id(self) -> builtins.str:
        '''The unique identifier for the segment.

        :cloudformationAttribute: SegmentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSegmentId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the segment is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0a8e1574ac5acde84da0f41e348c6e9d69019ecdea8a1211569fbe942d6916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the segment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ee366eaedd5d0b9cd71b45cdb646586561f77c8a288dfec57bb418a8361cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SegmentDimensionsProperty"]]:
        '''The criteria that define the dimensions for the segment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-dimensions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SegmentDimensionsProperty"]], jsii.get(self, "dimensions"))

    @dimensions.setter
    def dimensions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SegmentDimensionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb90f1653a3ccc9627597904756a80e4c93e27a5f84a85544f921e1b9936ef5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensions", value)

    @builtins.property
    @jsii.member(jsii_name="segmentGroups")
    def segment_groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SegmentGroupsProperty"]]:
        '''The segment group to use and the dimensions to apply to the group's base segments in order to build the segment.

        A segment group can consist of zero or more base segments. Your request can include only one segment group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-segmentgroups
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SegmentGroupsProperty"]], jsii.get(self, "segmentGroups"))

    @segment_groups.setter
    def segment_groups(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SegmentGroupsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf01cd98986d7b32e2d5189028538efed8d515cab1c84c5bce2ebc7c5c12923a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentGroups", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.AttributeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_type": "attributeType", "values": "values"},
    )
    class AttributeDimensionProperty:
        def __init__(
            self,
            *,
            attribute_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies attribute-based criteria for including or excluding endpoints from a segment.

            :param attribute_type: The type of segment dimension to use. Valid values are:. - ``INCLUSIVE`` – endpoints that have attributes matching the values are included in the segment. - ``EXCLUSIVE`` – endpoints that have attributes matching the values are excluded from the segment. - ``CONTAINS`` – endpoints that have attributes' substrings match the values are included in the segment. - ``BEFORE`` – endpoints with attributes read as ISO_INSTANT datetimes before the value are included in the segment. - ``AFTER`` – endpoints with attributes read as ISO_INSTANT datetimes after the value are included in the segment. - ``BETWEEN`` – endpoints with attributes read as ISO_INSTANT datetimes between the values are included in the segment. - ``ON`` – endpoints with attributes read as ISO_INSTANT dates on the value are included in the segment. Time is ignored in this comparison.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``AttributeType`` property, endpoints are included or excluded from the segment if their attribute values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                attribute_dimension_property = pinpoint.CfnSegment.AttributeDimensionProperty(
                    attribute_type="attributeType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83e1a3df206fc6996c714f281147d93537936eb6c07c697d3fec6d1fabed0c14)
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use. Valid values are:.

            - ``INCLUSIVE`` – endpoints that have attributes matching the values are included in the segment.
            - ``EXCLUSIVE`` – endpoints that have attributes matching the values are excluded from the segment.
            - ``CONTAINS`` – endpoints that have attributes' substrings match the values are included in the segment.
            - ``BEFORE`` – endpoints with attributes read as ISO_INSTANT datetimes before the value are included in the segment.
            - ``AFTER`` – endpoints with attributes read as ISO_INSTANT datetimes after the value are included in the segment.
            - ``BETWEEN`` – endpoints with attributes read as ISO_INSTANT datetimes between the values are included in the segment.
            - ``ON`` – endpoints with attributes read as ISO_INSTANT dates on the value are included in the segment. Time is ignored in this comparison.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html#cfn-pinpoint-segment-attributedimension-attributetype
            '''
            result = self._values.get("attribute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``AttributeType`` property, endpoints are included or excluded from the segment if their attribute values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html#cfn-pinpoint-segment-attributedimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.BehaviorProperty",
        jsii_struct_bases=[],
        name_mapping={"recency": "recency"},
    )
    class BehaviorProperty:
        def __init__(
            self,
            *,
            recency: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.RecencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies behavior-based criteria for the segment, such as how recently users have used your app.

            :param recency: Specifies how recently segment members were active.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                behavior_property = pinpoint.CfnSegment.BehaviorProperty(
                    recency=pinpoint.CfnSegment.RecencyProperty(
                        duration="duration",
                        recency_type="recencyType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9eec04bc94fd19713678447dbc443534c19776a0279e89e9c033e829a1e6f6a8)
                check_type(argname="argument recency", value=recency, expected_type=type_hints["recency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recency is not None:
                self._values["recency"] = recency

        @builtins.property
        def recency(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.RecencyProperty"]]:
            '''Specifies how recently segment members were active.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency
            '''
            result = self._values.get("recency")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.RecencyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BehaviorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.CoordinatesProperty",
        jsii_struct_bases=[],
        name_mapping={"latitude": "latitude", "longitude": "longitude"},
    )
    class CoordinatesProperty:
        def __init__(self, *, latitude: jsii.Number, longitude: jsii.Number) -> None:
            '''Specifies the GPS coordinates of a location.

            :param latitude: The latitude coordinate of the location.
            :param longitude: The longitude coordinate of the location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                coordinates_property = pinpoint.CfnSegment.CoordinatesProperty(
                    latitude=123,
                    longitude=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca4ec94323fbf3593aadcece503e2d7e202effa77c20d958789c0b45aca80678)
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "latitude": latitude,
                "longitude": longitude,
            }

        @builtins.property
        def latitude(self) -> jsii.Number:
            '''The latitude coordinate of the location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates-latitude
            '''
            result = self._values.get("latitude")
            assert result is not None, "Required property 'latitude' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def longitude(self) -> jsii.Number:
            '''The longitude coordinate of the location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates-longitude
            '''
            result = self._values.get("longitude")
            assert result is not None, "Required property 'longitude' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoordinatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.DemographicProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_version": "appVersion",
            "channel": "channel",
            "device_type": "deviceType",
            "make": "make",
            "model": "model",
            "platform": "platform",
        },
    )
    class DemographicProperty:
        def __init__(
            self,
            *,
            app_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            channel: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            device_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            make: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            model: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            platform: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies demographic-based criteria, such as device platform, for the segment.

            :param app_version: The app version criteria for the segment.
            :param channel: The channel criteria for the segment.
            :param device_type: The device type criteria for the segment.
            :param make: The device make criteria for the segment.
            :param model: The device model criteria for the segment.
            :param platform: The device platform criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                demographic_property = pinpoint.CfnSegment.DemographicProperty(
                    app_version=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    channel=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    device_type=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    make=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    model=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    platform=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c02d0e32ebdbe792d8ac0c08756a24a44927af6aa8185756c3a14f1a618d235)
                check_type(argname="argument app_version", value=app_version, expected_type=type_hints["app_version"])
                check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
                check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
                check_type(argname="argument make", value=make, expected_type=type_hints["make"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_version is not None:
                self._values["app_version"] = app_version
            if channel is not None:
                self._values["channel"] = channel
            if device_type is not None:
                self._values["device_type"] = device_type
            if make is not None:
                self._values["make"] = make
            if model is not None:
                self._values["model"] = model
            if platform is not None:
                self._values["platform"] = platform

        @builtins.property
        def app_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]]:
            '''The app version criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-appversion
            '''
            result = self._values.get("app_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]], result)

        @builtins.property
        def channel(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]]:
            '''The channel criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-channel
            '''
            result = self._values.get("channel")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]], result)

        @builtins.property
        def device_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]]:
            '''The device type criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-devicetype
            '''
            result = self._values.get("device_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]], result)

        @builtins.property
        def make(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]]:
            '''The device make criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-make
            '''
            result = self._values.get("make")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]], result)

        @builtins.property
        def model(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]]:
            '''The device model criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]], result)

        @builtins.property
        def platform(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]]:
            '''The device platform criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-platform
            '''
            result = self._values.get("platform")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DemographicProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.GPSPointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "coordinates": "coordinates",
            "range_in_kilometers": "rangeInKilometers",
        },
    )
    class GPSPointProperty:
        def __init__(
            self,
            *,
            coordinates: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.CoordinatesProperty", typing.Dict[builtins.str, typing.Any]]],
            range_in_kilometers: jsii.Number,
        ) -> None:
            '''Specifies the GPS coordinates of the endpoint location.

            :param coordinates: The GPS coordinates to measure distance from.
            :param range_in_kilometers: The range, in kilometers, from the GPS coordinates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                g_pSPoint_property = pinpoint.CfnSegment.GPSPointProperty(
                    coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                        latitude=123,
                        longitude=123
                    ),
                    range_in_kilometers=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b1008e78bcf6ae7076bdcee0fa4c0d6db3875241ca67f0b48ccd700fd925c33)
                check_type(argname="argument coordinates", value=coordinates, expected_type=type_hints["coordinates"])
                check_type(argname="argument range_in_kilometers", value=range_in_kilometers, expected_type=type_hints["range_in_kilometers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "coordinates": coordinates,
                "range_in_kilometers": range_in_kilometers,
            }

        @builtins.property
        def coordinates(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.CoordinatesProperty"]:
            '''The GPS coordinates to measure distance from.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates
            '''
            result = self._values.get("coordinates")
            assert result is not None, "Required property 'coordinates' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.CoordinatesProperty"], result)

        @builtins.property
        def range_in_kilometers(self) -> jsii.Number:
            '''The range, in kilometers, from the GPS coordinates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-rangeinkilometers
            '''
            result = self._values.get("range_in_kilometers")
            assert result is not None, "Required property 'range_in_kilometers' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GPSPointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.GroupsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "source_segments": "sourceSegments",
            "source_type": "sourceType",
            "type": "type",
        },
    )
    class GroupsProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SegmentDimensionsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_segments: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SourceSegmentsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_type: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An array that defines the set of segment criteria to evaluate when handling segment groups for the segment.

            :param dimensions: An array that defines the dimensions to include or exclude from the segment.
            :param source_segments: The base segment to build the segment on. A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify. You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.
            :param source_type: Specifies how to handle multiple base segments for the segment. For example, if you specify three base segments for the segment, whether the resulting segment is based on all, any, or none of the base segments.
            :param type: Specifies how to handle multiple dimensions for the segment. For example, if you specify three dimensions for the segment, whether the resulting segment includes endpoints that match all, any, or none of the dimensions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                groups_property = pinpoint.CfnSegment.GroupsProperty(
                    dimensions=[pinpoint.CfnSegment.SegmentDimensionsProperty(
                        attributes=attributes,
                        behavior=pinpoint.CfnSegment.BehaviorProperty(
                            recency=pinpoint.CfnSegment.RecencyProperty(
                                duration="duration",
                                recency_type="recencyType"
                            )
                        ),
                        demographic=pinpoint.CfnSegment.DemographicProperty(
                            app_version=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            channel=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            device_type=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            make=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            model=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            platform=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        location=pinpoint.CfnSegment.LocationProperty(
                            country=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            gps_point=pinpoint.CfnSegment.GPSPointProperty(
                                coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                    latitude=123,
                                    longitude=123
                                ),
                                range_in_kilometers=123
                            )
                        ),
                        metrics=metrics,
                        user_attributes=user_attributes
                    )],
                    source_segments=[pinpoint.CfnSegment.SourceSegmentsProperty(
                        id="id",
                
                        # the properties below are optional
                        version=123
                    )],
                    source_type="sourceType",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9e2814269a21f322e99c218a52c06bd34848cb6fd92554e63f0acd87cead2e4)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument source_segments", value=source_segments, expected_type=type_hints["source_segments"])
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if source_segments is not None:
                self._values["source_segments"] = source_segments
            if source_type is not None:
                self._values["source_type"] = source_type
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SegmentDimensionsProperty"]]]]:
            '''An array that defines the dimensions to include or exclude from the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SegmentDimensionsProperty"]]]], result)

        @builtins.property
        def source_segments(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SourceSegmentsProperty"]]]]:
            '''The base segment to build the segment on.

            A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify.

            You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments
            '''
            result = self._values.get("source_segments")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SourceSegmentsProperty"]]]], result)

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple base segments for the segment.

            For example, if you specify three base segments for the segment, whether the resulting segment is based on all, any, or none of the base segments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple dimensions for the segment.

            For example, if you specify three dimensions for the segment, whether the resulting segment includes endpoints that match all, any, or none of the dimensions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"country": "country", "gps_point": "gpsPoint"},
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            country: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            gps_point: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.GPSPointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies location-based criteria, such as region or GPS coordinates, for the segment.

            :param country: The country or region code, in ISO 3166-1 alpha-2 format, for the segment.
            :param gps_point: The GPS point dimension for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                location_property = pinpoint.CfnSegment.LocationProperty(
                    country=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    gps_point=pinpoint.CfnSegment.GPSPointProperty(
                        coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                            latitude=123,
                            longitude=123
                        ),
                        range_in_kilometers=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03da39b2fc02da543c928064697aa37ea085d1266b04bb92464482904a073b6c)
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument gps_point", value=gps_point, expected_type=type_hints["gps_point"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if country is not None:
                self._values["country"] = country
            if gps_point is not None:
                self._values["gps_point"] = gps_point

        @builtins.property
        def country(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]]:
            '''The country or region code, in ISO 3166-1 alpha-2 format, for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html#cfn-pinpoint-segment-segmentdimensions-location-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.SetDimensionProperty"]], result)

        @builtins.property
        def gps_point(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.GPSPointProperty"]]:
            '''The GPS point dimension for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint
            '''
            result = self._values.get("gps_point")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.GPSPointProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.RecencyProperty",
        jsii_struct_bases=[],
        name_mapping={"duration": "duration", "recency_type": "recencyType"},
    )
    class RecencyProperty:
        def __init__(
            self,
            *,
            duration: builtins.str,
            recency_type: builtins.str,
        ) -> None:
            '''Specifies how recently segment members were active.

            :param duration: The duration to use when determining which users have been active or inactive with your app. Possible values: ``HR_24`` | ``DAY_7`` | ``DAY_14`` | ``DAY_30`` .
            :param recency_type: The type of recency dimension to use for the segment. Valid values are: ``ACTIVE`` and ``INACTIVE`` . If the value is ``ACTIVE`` , the segment includes users who have used your app within the specified duration are included in the segment. If the value is ``INACTIVE`` , the segment includes users who haven't used your app within the specified duration are included in the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                recency_property = pinpoint.CfnSegment.RecencyProperty(
                    duration="duration",
                    recency_type="recencyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ed252f3a3e8528df90cd7c6e4598509ad62fc1d1abb326877aed598872a04f1)
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument recency_type", value=recency_type, expected_type=type_hints["recency_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "duration": duration,
                "recency_type": recency_type,
            }

        @builtins.property
        def duration(self) -> builtins.str:
            '''The duration to use when determining which users have been active or inactive with your app.

            Possible values: ``HR_24`` | ``DAY_7`` | ``DAY_14`` | ``DAY_30`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency-duration
            '''
            result = self._values.get("duration")
            assert result is not None, "Required property 'duration' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def recency_type(self) -> builtins.str:
            '''The type of recency dimension to use for the segment.

            Valid values are: ``ACTIVE`` and ``INACTIVE`` . If the value is ``ACTIVE`` , the segment includes users who have used your app within the specified duration are included in the segment. If the value is ``INACTIVE`` , the segment includes users who haven't used your app within the specified duration are included in the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency-recencytype
            '''
            result = self._values.get("recency_type")
            assert result is not None, "Required property 'recency_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.SegmentDimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "behavior": "behavior",
            "demographic": "demographic",
            "location": "location",
            "metrics": "metrics",
            "user_attributes": "userAttributes",
        },
    )
    class SegmentDimensionsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            behavior: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.BehaviorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            demographic: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.DemographicProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metrics: typing.Any = None,
            user_attributes: typing.Any = None,
        ) -> None:
            '''Specifies the dimension settings for a segment.

            :param attributes: One or more custom attributes to use as criteria for the segment.
            :param behavior: The behavior-based criteria, such as how recently users have used your app, for the segment.
            :param demographic: The demographic-based criteria, such as device platform, for the segment.
            :param location: The location-based criteria, such as region or GPS coordinates, for the segment.
            :param metrics: One or more custom metrics to use as criteria for the segment.
            :param user_attributes: One or more custom user attributes to use as criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                segment_dimensions_property = pinpoint.CfnSegment.SegmentDimensionsProperty(
                    attributes=attributes,
                    behavior=pinpoint.CfnSegment.BehaviorProperty(
                        recency=pinpoint.CfnSegment.RecencyProperty(
                            duration="duration",
                            recency_type="recencyType"
                        )
                    ),
                    demographic=pinpoint.CfnSegment.DemographicProperty(
                        app_version=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        channel=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        device_type=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        make=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        model=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        platform=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    location=pinpoint.CfnSegment.LocationProperty(
                        country=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        gps_point=pinpoint.CfnSegment.GPSPointProperty(
                            coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                latitude=123,
                                longitude=123
                            ),
                            range_in_kilometers=123
                        )
                    ),
                    metrics=metrics,
                    user_attributes=user_attributes
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d312738042a72923349fd29b0e94bd1d8150a918330ada6380b5eed0ffff9b00)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
                check_type(argname="argument demographic", value=demographic, expected_type=type_hints["demographic"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                check_type(argname="argument user_attributes", value=user_attributes, expected_type=type_hints["user_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if behavior is not None:
                self._values["behavior"] = behavior
            if demographic is not None:
                self._values["demographic"] = demographic
            if location is not None:
                self._values["location"] = location
            if metrics is not None:
                self._values["metrics"] = metrics
            if user_attributes is not None:
                self._values["user_attributes"] = user_attributes

        @builtins.property
        def attributes(self) -> typing.Any:
            '''One or more custom attributes to use as criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Any, result)

        @builtins.property
        def behavior(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.BehaviorProperty"]]:
            '''The behavior-based criteria, such as how recently users have used your app, for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-behavior
            '''
            result = self._values.get("behavior")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.BehaviorProperty"]], result)

        @builtins.property
        def demographic(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.DemographicProperty"]]:
            '''The demographic-based criteria, such as device platform, for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-demographic
            '''
            result = self._values.get("demographic")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.DemographicProperty"]], result)

        @builtins.property
        def location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.LocationProperty"]]:
            '''The location-based criteria, such as region or GPS coordinates, for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.LocationProperty"]], result)

        @builtins.property
        def metrics(self) -> typing.Any:
            '''One or more custom metrics to use as criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Any, result)

        @builtins.property
        def user_attributes(self) -> typing.Any:
            '''One or more custom user attributes to use as criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-userattributes
            '''
            result = self._values.get("user_attributes")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentDimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.SegmentGroupsProperty",
        jsii_struct_bases=[],
        name_mapping={"groups": "groups", "include": "include"},
    )
    class SegmentGroupsProperty:
        def __init__(
            self,
            *,
            groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSegment.GroupsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the set of segment criteria to evaluate when handling segment groups for the segment.

            :param groups: Specifies the set of segment criteria to evaluate when handling segment groups for the segment.
            :param include: Specifies how to handle multiple segment groups for the segment. For example, if the segment includes three segment groups, whether the resulting segment includes endpoints that match all, any, or none of the segment groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                segment_groups_property = pinpoint.CfnSegment.SegmentGroupsProperty(
                    groups=[pinpoint.CfnSegment.GroupsProperty(
                        dimensions=[pinpoint.CfnSegment.SegmentDimensionsProperty(
                            attributes=attributes,
                            behavior=pinpoint.CfnSegment.BehaviorProperty(
                                recency=pinpoint.CfnSegment.RecencyProperty(
                                    duration="duration",
                                    recency_type="recencyType"
                                )
                            ),
                            demographic=pinpoint.CfnSegment.DemographicProperty(
                                app_version=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                channel=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                device_type=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                make=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                model=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                platform=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            location=pinpoint.CfnSegment.LocationProperty(
                                country=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                gps_point=pinpoint.CfnSegment.GPSPointProperty(
                                    coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                        latitude=123,
                                        longitude=123
                                    ),
                                    range_in_kilometers=123
                                )
                            ),
                            metrics=metrics,
                            user_attributes=user_attributes
                        )],
                        source_segments=[pinpoint.CfnSegment.SourceSegmentsProperty(
                            id="id",
                
                            # the properties below are optional
                            version=123
                        )],
                        source_type="sourceType",
                        type="type"
                    )],
                    include="include"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b42e1c0aa74d6e146120b91e8c3e5a61594133291e67f4772127e226ed7e8478)
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if groups is not None:
                self._values["groups"] = groups
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.GroupsProperty"]]]]:
            '''Specifies the set of segment criteria to evaluate when handling segment groups for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html#cfn-pinpoint-segment-segmentgroups-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSegment.GroupsProperty"]]]], result)

        @builtins.property
        def include(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple segment groups for the segment.

            For example, if the segment includes three segment groups, whether the resulting segment includes endpoints that match all, any, or none of the segment groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html#cfn-pinpoint-segment-segmentgroups-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentGroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.SetDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class SetDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the dimension type and values for a segment dimension.

            :param dimension_type: The type of segment dimension to use. Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                set_dimension_property = pinpoint.CfnSegment.SetDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29af47784f33f34fc467d78482e24361671a1ceeded8ab66e7e8d21e1031f8f0)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use.

            Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html#cfn-pinpoint-segment-setdimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html#cfn-pinpoint-segment-setdimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-pinpoint.CfnSegment.SourceSegmentsProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "version": "version"},
    )
    class SourceSegmentsProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the base segment to build the segment on.

            A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify.

            You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.

            :param id: The unique identifier for the source segment.
            :param version: The version number of the source segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_pinpoint as pinpoint
                
                source_segments_property = pinpoint.CfnSegment.SourceSegmentsProperty(
                    id="id",
                
                    # the properties below are optional
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9cd74be6bcbf3ee8ca9a4faf45de34d975ca0a33ef9d6cbd4bd1b0a8558104cb)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def id(self) -> builtins.str:
            '''The unique identifier for the source segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''The version number of the source segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceSegmentsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnSegmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "name": "name",
        "dimensions": "dimensions",
        "segment_groups": "segmentGroups",
        "tags": "tags",
    },
)
class CfnSegmentProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        name: builtins.str,
        dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        segment_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SegmentGroupsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnSegment``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the segment is associated with.
        :param name: The name of the segment.
        :param dimensions: The criteria that define the dimensions for the segment.
        :param segment_groups: The segment group to use and the dimensions to apply to the group's base segments in order to build the segment. A segment group can consist of zero or more base segments. Your request can include only one segment group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            # attributes: Any
            # metrics: Any
            # tags: Any
            # user_attributes: Any
            
            cfn_segment_props = pinpoint.CfnSegmentProps(
                application_id="applicationId",
                name="name",
            
                # the properties below are optional
                dimensions=pinpoint.CfnSegment.SegmentDimensionsProperty(
                    attributes=attributes,
                    behavior=pinpoint.CfnSegment.BehaviorProperty(
                        recency=pinpoint.CfnSegment.RecencyProperty(
                            duration="duration",
                            recency_type="recencyType"
                        )
                    ),
                    demographic=pinpoint.CfnSegment.DemographicProperty(
                        app_version=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        channel=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        device_type=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        make=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        model=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        platform=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    location=pinpoint.CfnSegment.LocationProperty(
                        country=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        gps_point=pinpoint.CfnSegment.GPSPointProperty(
                            coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                latitude=123,
                                longitude=123
                            ),
                            range_in_kilometers=123
                        )
                    ),
                    metrics=metrics,
                    user_attributes=user_attributes
                ),
                segment_groups=pinpoint.CfnSegment.SegmentGroupsProperty(
                    groups=[pinpoint.CfnSegment.GroupsProperty(
                        dimensions=[pinpoint.CfnSegment.SegmentDimensionsProperty(
                            attributes=attributes,
                            behavior=pinpoint.CfnSegment.BehaviorProperty(
                                recency=pinpoint.CfnSegment.RecencyProperty(
                                    duration="duration",
                                    recency_type="recencyType"
                                )
                            ),
                            demographic=pinpoint.CfnSegment.DemographicProperty(
                                app_version=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                channel=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                device_type=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                make=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                model=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                platform=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            location=pinpoint.CfnSegment.LocationProperty(
                                country=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                gps_point=pinpoint.CfnSegment.GPSPointProperty(
                                    coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                        latitude=123,
                                        longitude=123
                                    ),
                                    range_in_kilometers=123
                                )
                            ),
                            metrics=metrics,
                            user_attributes=user_attributes
                        )],
                        source_segments=[pinpoint.CfnSegment.SourceSegmentsProperty(
                            id="id",
            
                            # the properties below are optional
                            version=123
                        )],
                        source_type="sourceType",
                        type="type"
                    )],
                    include="include"
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d585e38801e9b6deff4ac553d1071c24b8dda1e50267a4f728e0526c1b56f47)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument segment_groups", value=segment_groups, expected_type=type_hints["segment_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "name": name,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if segment_groups is not None:
            self._values["segment_groups"] = segment_groups
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the segment is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the segment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSegment.SegmentDimensionsProperty]]:
        '''The criteria that define the dimensions for the segment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-dimensions
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSegment.SegmentDimensionsProperty]], result)

    @builtins.property
    def segment_groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSegment.SegmentGroupsProperty]]:
        '''The segment group to use and the dimensions to apply to the group's base segments in order to build the segment.

        A segment group can consist of zero or more base segments. Your request can include only one segment group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-segmentgroups
        '''
        result = self._values.get("segment_groups")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSegment.SegmentGroupsProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSegmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSmsTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnSmsTemplate",
):
    '''A CloudFormation ``AWS::Pinpoint::SmsTemplate``.

    Creates a message template that you can use in messages that are sent through the SMS channel. A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :cloudformationResource: AWS::Pinpoint::SmsTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        # tags: Any
        
        cfn_sms_template = pinpoint.CfnSmsTemplate(self, "MyCfnSmsTemplate",
            body="body",
            template_name="templateName",
        
            # the properties below are optional
            default_substitutions="defaultSubstitutions",
            tags=tags,
            template_description="templateDescription"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        body: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::SmsTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param body: The message body to use in text messages that are based on the message template.
        :param template_name: The name of the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045e711f6ffe3f80379408f380b368a8b20279c46fafa222266842b600a2bd7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSmsTemplateProps(
            body=body,
            template_name=template_name,
            default_substitutions=default_substitutions,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743ac17eb423e4f82cf1a8753bdc59bf131f0b00832b4b8ca27fcff976b64423)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a8f6881df5a9d9b4389595d39af93a26548dd82a35626d4e6069818603d4d71)
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
        '''The Amazon Resource Name (ARN) of the message template.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        '''The message body to use in text messages that are based on the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-body
        '''
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf4352a92db77d953227e7523aefbc0fd61fc2b53806b5d9033aa1d11a0ccf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatename
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079b700c5a8d10acb8e7fe17a8d99e3584d3b67b84055e178278fe95dd000792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-defaultsubstitutions
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSubstitutions"))

    @default_substitutions.setter
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6fbc34e4ef91f94707b3b93c20827ecbe498ee695470a70a92e3ae12db3833d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatedescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0195246c72c42c437f2f81a73dda3b8844c00948a5d4e418bd184ccba381bb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnSmsTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "body": "body",
        "template_name": "templateName",
        "default_substitutions": "defaultSubstitutions",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnSmsTemplateProps:
    def __init__(
        self,
        *,
        body: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSmsTemplate``.

        :param body: The message body to use in text messages that are based on the message template.
        :param template_name: The name of the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            # tags: Any
            
            cfn_sms_template_props = pinpoint.CfnSmsTemplateProps(
                body="body",
                template_name="templateName",
            
                # the properties below are optional
                default_substitutions="defaultSubstitutions",
                tags=tags,
                template_description="templateDescription"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e77c53201ce08e15813d7f687acc3aa4a18801d783ec3d0f0455b8429c17828)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "body": body,
            "template_name": template_name,
        }
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def body(self) -> builtins.str:
        '''The message body to use in text messages that are based on the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-body
        '''
        result = self._values.get("body")
        assert result is not None, "Required property 'body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSmsTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVoiceChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pinpoint.CfnVoiceChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::VoiceChannel``.

    A *channel* is a type of platform that you can deliver messages to. To send a voice message, you send the message through the voice channel. Before you can use Amazon Pinpoint to send voice messages, you have to enable the voice channel for an Amazon Pinpoint application.

    The VoiceChannel resource represents the status and other information about the voice channel for an application.

    :cloudformationResource: AWS::Pinpoint::VoiceChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pinpoint as pinpoint
        
        cfn_voice_channel = pinpoint.CfnVoiceChannel(self, "MyCfnVoiceChannel",
            application_id="applicationId",
        
            # the properties below are optional
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::VoiceChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the voice channel applies to.
        :param enabled: Specifies whether to enable the voice channel for the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1749026481cd71ef82009ec72de8b742285669d58162253b782b25af040107d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVoiceChannelProps(application_id=application_id, enabled=enabled)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4144c17931e8ba753cceec21e16fb551e637f7972ad3c90d7878c0db5409c692)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e091058e96733c9d30618a2df15e339da29c39292f62111e207083da8bef9363)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the voice channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d770a12affe72d165755a98a2eb69adda9ed75395c551965177164023006922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the voice channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa629f76a0d979c8a6cb0751e8bd5153c8fbcc8faa5fcafdc7d7a9230b74e917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pinpoint.CfnVoiceChannelProps",
    jsii_struct_bases=[],
    name_mapping={"application_id": "applicationId", "enabled": "enabled"},
)
class CfnVoiceChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVoiceChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the voice channel applies to.
        :param enabled: Specifies whether to enable the voice channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pinpoint as pinpoint
            
            cfn_voice_channel_props = pinpoint.CfnVoiceChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dbb601524c56bff5fa26ae1812175c95bcc222257fdfceab8fca30efeb1bf2d)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the voice channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to enable the voice channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVoiceChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnADMChannel",
    "CfnADMChannelProps",
    "CfnAPNSChannel",
    "CfnAPNSChannelProps",
    "CfnAPNSSandboxChannel",
    "CfnAPNSSandboxChannelProps",
    "CfnAPNSVoipChannel",
    "CfnAPNSVoipChannelProps",
    "CfnAPNSVoipSandboxChannel",
    "CfnAPNSVoipSandboxChannelProps",
    "CfnApp",
    "CfnAppProps",
    "CfnApplicationSettings",
    "CfnApplicationSettingsProps",
    "CfnBaiduChannel",
    "CfnBaiduChannelProps",
    "CfnCampaign",
    "CfnCampaignProps",
    "CfnEmailChannel",
    "CfnEmailChannelProps",
    "CfnEmailTemplate",
    "CfnEmailTemplateProps",
    "CfnEventStream",
    "CfnEventStreamProps",
    "CfnGCMChannel",
    "CfnGCMChannelProps",
    "CfnInAppTemplate",
    "CfnInAppTemplateProps",
    "CfnPushTemplate",
    "CfnPushTemplateProps",
    "CfnSMSChannel",
    "CfnSMSChannelProps",
    "CfnSegment",
    "CfnSegmentProps",
    "CfnSmsTemplate",
    "CfnSmsTemplateProps",
    "CfnVoiceChannel",
    "CfnVoiceChannelProps",
]

publication.publish()

def _typecheckingstub__89edf7657f2dc9f670d88e0dec8cfcdc9581aa90914d2fbc0740cc5b0b3684c5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ff400797b6af54e2f2d3c814d120e8481cc789961dbd74cf0247eb76a8aa42(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083070488dc8a3a1931e8c3c551a3eda6b3d1dd55c4a0f5503e92fbb25c0f8c2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c7d63916548b2a6b7e6e97faba0331d844d3371e9665c0ce8112a4ff5e8ae8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea31fb98f19d82b67b3ead2a86c75157d3c035e8955e97b62d438df00382ab89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808f1624697403c9bfbde0547b92a6655474619708864d71409ffa5fed93bc5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8c7f61c0f0495f977773a1a5558cbcdf5462444a65e68f085a2f1ce5e10a96(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd63651bdc32d38170be7c4a4ea62566f564977bb03c5be3bc885bbd0cb4b2ad(
    *,
    application_id: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9feda3513378ee7fef3c8c73037158787d185952d582ff1d512313660b5dbf0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549a6e427ed22bf2722c1530341ccb5c8731351051e45613d62a97512e5353c7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbf18ec330cbafb33e965633cf7f20d2989b90762d2689e87d80313dd2d3cf5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31abf31a748027b68f1c4a64decf362d8e81293755e50cab38fcafb60b78d5f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33058b558e8b0e12e81768ce69e2884234f2eeb4127087c9187e30abf36832ba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ef6ff9c72c4b1b3764a80c5d829db3642e11c6fd5aa35ed51e904d898ca026(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09937094f310fa7f154a19107081618c010e7c0a0315778a8429bd4213c074da(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4a195981c1f67de79a8a3e8ea152a7fa2337d3cc1f42fca84002df3de0381d(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099692d77a41da495fb6ea6c75c2f338b3bf6aea24719f52c296c0614ded53ae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d191bea5990946338f62313d34a933cd099da0a14b35c1711698f58576a8c7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c508dfee6a703b62c905e6c6f3cdf517ff0f2b1c10eef24ba9d037ea4f4edb37(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa16b10aeccbaec0fbfc0c09826479294f7844fadaef7478f11734d1d856a54c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df1012692ddb95edd94a29e46e3c37bde870b6b39cf2ed492aeca9a98c9174e(
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df97cce65ed8aaf553b9054297eb52594bf98f44af0b32fa02822147c8f4ca4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc43c02fb32e7af990c8eb8e2d163c1bea0a3ec6ccd3fde5678b68604ed09e8(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0218f15734a3890a35ed3acdff40abc74e04d7a45fd18a9d85dadd7b19b8f219(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6206f551682501c583efaa443f65098ac5afefd1cfc7de199e2e2993424c714a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9767f7fc70860d849070a5b642b96885183f62eeef538b2d9dfa83347a0ddd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b96de92128eecce5d4a3d24f1b3dca6381dfddb6971061a10a78e85e4158805(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4dcbeb2f35cb493fdec1205723efabab5a2b709eb31237c502ac5d5618b0f3d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3081fe81131829bb7ee65429e89ffa73c0ded99af807b98d1535543d19e397b6(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85c9977ecd52bbd3954500b80fcfea9b850085e111b606b190ba46cf9562180(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865d16a41042cf472e4157a0175c083a52433b4013f88ca69de890d5eaee17bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52663a851c27d4ccdd4b2c4ded455f019567b5807157a41c57b009de8be9f79(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadb03b9f90459ed52ee988277fe121bb2dff301a0f6cea8a1a9b6dbeed37d4f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411b5bef1c3d579e00dd53ac839ad5a1c6a3b157fd563191814177fab9c24f77(
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23406e640ee8559d65d605cf6019e589ca1f122cd388387a80adc1925eb73769(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6676c9280805c25076072ae0326cffa05dd8471a01e4dd4be0711466a3d58eeb(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880fc2f7e4f8b2a9f24e91dd282350faadbaa03dd37ccc77ca647eb101c6eba5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92dac5bbc68e29ed312064e45d44376582fbeb28bd83d7af1d2ab210309ddb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72df9ddff41ffbcc6c8c89aabb0077ae2ea9a90657d4b65a0eff889c0783858(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9c46429af8a3a4f4bca70143a869245dab91385cffa27794b3a1d178269b64(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1559b15b2148192307edd48d114f38aefefd9e53082b84d6ea4312552afe4d62(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e1e94ef8d29e3ab5cde7c8f72d06b8290d334d526d87f6d2fdf2c006d875ac(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d29f21761a33e992d22f076f1bb6a0acc87140fc506ccef8bd5f187354f351(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d349da5eebb40c1d34d92c7ab3611b362c2234ff4d8c29af1c17d2893611f24e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ee4183b1669eab7d1171c938c4685f2c53512f43e03a448716f966aa21b76d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41098345792d576241caac84f1711e120d64963b3e30f223926621003522a77f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f2664afa90492fb1bbb2a91abd1a44b2e09a85874925d509d55be50ff67a0f(
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb121d47466f6ab933fdba78a10babeee30fe2e5d4f9385be72b0968cff8fc8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c66e56ccb64009018dc4f00616d2d80b181ff814f6c41919eee8a383e4be4c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115c73adc974eeaa28e0097b9852b287746c56bf189263dfb1222395c3680851(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c372c52dee15e202b12adc6834e5e4c1acf718a0b729fb2fb0235ce20a17c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed65bf4387c96499a3d56399003709f17bb281c0a37d48d72b7034402f6e039(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f826be23fe72cd9df2e36b34c119783db08e0f83e699d2c0443e5bfff724a573(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468af95861da2dfcfcdc705468190cdd8f6c12163f8461c1f98ec218f8224e91(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2355b430e7729e890a58439a96ed13ccedfe88064ff7160c89b1fe4be5cc49(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2498da1460d4b163a22fb98a4810c9e6ad3a0cb9e58e0f7d83059a7bc89d7566(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8822b3b59b5cd7ee3ce26d710ce38acf1f442d0a46a3c5383e1230bf990352d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e5f1eeed61d8c7aff29f9f5189c94269b7900569f4a87f198c94c1bd1bb20b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436070a4aeed9b794640b0ee686010965402379283f2e4e922ed8bf6b1fb8fbc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b99e4cd78c895269dbe48d9f84ff34d894b35642cc012e927d3d770bcf66ee(
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498e015913faa51042166627026ab7531855376d5c70623d211ce1ec8a74dc7d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ed1a25988742ce022a803761f9650e64e228bde96f12e192ff6584692d05b4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8483cf96c83ad5d24abd9ce0ee83fe485d71f6973a042b0d79a7b5b824c1b8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd57e24f1f8059648325e2e6c6ce87380ca1795f817ad928cead51fb90be5f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a33a4ae44d4e8f6fa7a80007fffc14e3a26d5b9ab8024c3142107b792f1ddc8(
    *,
    name: builtins.str,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4a69f1b475b10bba93b972e6b823e3e22ebf7d1a3d5d35427ed7dbc12ff6e5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    campaign_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    limits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.LimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    quiet_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4e7900110fae058427efccfbfa284f4572d4988df7a17be671d86debe0c866(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a9bf62737da228011aabc0ffd0ae507513561025e10d9c9637e3f9b44687e5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e8fb56da298578ca8d39c9c724261d97457df5b34e852a54598f6ca319976a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74976d0ff12837f5338928827e51fb9c721668e97e7428ddf1dc20485880b56a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.CampaignHookProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c45868d9d830dab662d4e5882d69b5cbf3567bef5e727946d301776193bd3d4(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3bb5b9589b8d6052708702f064d21841b15fce11748395a8f9a03db14ccd634(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.LimitsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0596480f4edc84656225446717bc11b496418f6149b5df27ae0c961d32ee0a90(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationSettings.QuietTimeProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e92f57ddd653aa16dba3f02196d1f66b04f83e5b03fa202375cb584fa114a63(
    *,
    lambda_function_name: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    web_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd4b78bc4370a1e61236d8e16f00207cf1ee14ee038f1540751d8991636ccd1(
    *,
    daily: typing.Optional[jsii.Number] = None,
    maximum_duration: typing.Optional[jsii.Number] = None,
    messages_per_second: typing.Optional[jsii.Number] = None,
    total: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967e7415ae200a01b9ddb4f52f65a8ac594028cec75d8637eefeb659e62a862e(
    *,
    end: builtins.str,
    start: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4d4d3fb7dea08b491541e3b25658722b92ae0c1965b3a4b8a6cb694ae65245(
    *,
    application_id: builtins.str,
    campaign_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    limits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.LimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    quiet_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationSettings.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e4017fb957107ef8edfac95ebf5b2c89d8de19ee66002f32583e24c05715f3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    api_key: builtins.str,
    application_id: builtins.str,
    secret_key: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9623bf6b3a79eb66f3076d81ee282f245d20577ee5b663dd9b3fb98eb3835d8f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5225e971f544ea5ab60cbef67dc740c41f3b34609a8c4fa2df06264c3e4319f7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58453759e3455ec47c00b3d46c422ff22d72834dc9b0b0162b1d0942c539161b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95629246d13954f399a65391512c09dc9e7221851a80d123429457f3021868d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c680b38c8525862cd812eaa73e1ba790ae155f40b4fd698335bd022cd85816db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9df32be297a3d2b631fc1217d6fd36e99182f2a0aab77905d148978f445d18f(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9c40921b2a9b6d7761eed64f65ef3fc23a95a7afdd25bb6e960e74f3b73213(
    *,
    api_key: builtins.str,
    application_id: builtins.str,
    secret_key: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f312ba8488922bb988cded7e2490b7e0c6ed68b18df08cd55e88808792af98(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    name: builtins.str,
    schedule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]],
    segment_id: builtins.str,
    additional_treatments: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.WriteTreatmentResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    campaign_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    holdout_percent: typing.Optional[jsii.Number] = None,
    is_paused: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    limits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.LimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    message_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    segment_version: typing.Optional[jsii.Number] = None,
    tags: typing.Any = None,
    template_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    treatment_description: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0510e5453252f5aca1d2efa74566a0d6621d348a3ac30242190a550eb9097cc(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68ceef6f72b6889db39a0aae149934397474ea3d4375ba596546bb52fe3550a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a00b8f96c494829d8216144ce316931f8b9cc2a1af20690ae3c17fb6802b78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9f23cd386851b7432c427c076f1b740dcf28cd3ab21a3746e2c24d242ff7ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402dae6387dcbcf9d244bfe777309bd4a3732a876f78c1c2943a3be60ab3bd4f(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.ScheduleProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8197fa413cff5a608e0931a0adf3dcd51fd4d24dc28913cf1c20ef9cefcacf8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468639b5b0aecd36e6bafd0d020bc48cc5e5f1918afdcf195393dae29c116112(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.WriteTreatmentResourceProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b70a1a55856d85013ddc9a9c020bcc5397da9ab3656a14a0cf656d1367c541(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.CampaignHookProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d279c867d043711677cf90da2bf24804a0460b310eb1f972fe551778b46fa9b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.CustomDeliveryConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c80e19e37274cc6145ac6078d0d44dd4360008ef903f541c7ae53f26bcf327(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c21aa521d6b2340c52a6e0e57eb31979397dca86456d0812004fa834e05d0cf(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdb83ae5e091ddcb7ca324e504556a0293d978c1e1a51757c11f032306e77b5(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fc5294b0429581a813a969789c4c2ce6c779ab82519995d04a129429fd9879(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.LimitsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67aaefe46d0e026926b19b1f92238defe75978a3656316bb5bc4033ea1484a0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.MessageConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b915814949b0b9cba117adb87e309d6ea45a0b929fe82ca4179feb80d1f1fbad(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6347a994a4952dcd1174bb33aeee26f672afa001b878d34e0f8e1d33167d783(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690875121b95ffea809005b44a64172ca545deff9c710ee3590f873abd080fe8(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.TemplateConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0206bc47b41e759bb57da8f33eaceb37065ed5c326107ef8c237d94548ebc3f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d476178f7d3414340ac6392d0c5382b456c08e882f5547e02ffa7d68c8eae23(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4251d500dfda9df0d13af3b53dc2a58e7c18f9eb84171c7302cf20ef8fc3b209(
    *,
    attribute_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f3c5aa5c1d54a20fd1891660410759a3bad3d7d80c8ed6b4661cf8aca9fc8f(
    *,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f154ba157a4e14cc3e9c26384ba9e0c70c6170ffc9b304789bb167d11c13faa(
    *,
    body: typing.Optional[builtins.str] = None,
    from_address: typing.Optional[builtins.str] = None,
    html_body: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcf71d57091f65f8a430d19e4d41879a49ab3dc5b5d89878c469fe03e4d01b8(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.EventDimensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0991cfc3a3c4ffb7cafef1e0b8af172a82e348cc02f536fae664d444a0393912(
    *,
    lambda_function_name: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    web_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ad29224e0ae089c0e96535955dbbd2bf1ce9804daa612f3d30056d4db01cb5(
    *,
    content: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_config: typing.Any = None,
    layout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155eded46e7c94a5a9dd5f0964941d0c297f5d9db7a94349b034c6edfcef7be1(
    *,
    body: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    message_type: typing.Optional[builtins.str] = None,
    origination_number: typing.Optional[builtins.str] = None,
    sender_id: typing.Optional[builtins.str] = None,
    template_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8feab8abce0f08277c847a660a7ec8980b62f1d7aea8bb7157677d2d744fae(
    *,
    delivery_uri: typing.Optional[builtins.str] = None,
    endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08fcc3214998024dd043dce3cf9d2a66a6f95040bf12731bed23ed76489a9903(
    *,
    background_color: typing.Optional[builtins.str] = None,
    border_radius: typing.Optional[jsii.Number] = None,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12848ac9df7b383d00d6225849ef7982e3726e8f4b1e10ea95e90307de1e7f05(
    *,
    attributes: typing.Any = None,
    event_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798f78d2a50cdcae6b4b93b8977132f8bda3d8dc3a7ef93a5d4f5e5d9c55f4b0(
    *,
    alignment: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2acb8ebbfd23d801d4081a1e6f915a455fa8cc9851e8604710d576f7f10afd(
    *,
    android: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.DefaultButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ios: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1cf923fc276b77b363db06c8a5ccddd5dac458124e77d29786fe78ce8f5f7e(
    *,
    background_color: typing.Optional[builtins.str] = None,
    body_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.InAppMessageBodyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    header_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.InAppMessageHeaderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_url: typing.Optional[builtins.str] = None,
    primary_btn: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.InAppMessageButtonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secondary_btn: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.InAppMessageButtonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9de89d0e96f2ce72a8e1c85f8a5c8c1b829c2e831625f1ce68c1a35f420aef(
    *,
    alignment: typing.Optional[builtins.str] = None,
    header: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547273fb7d7d1dadd3428718b6a46ca495cf2fbebd24e52c67312c91f82a2098(
    *,
    daily: typing.Optional[jsii.Number] = None,
    maximum_duration: typing.Optional[jsii.Number] = None,
    messages_per_second: typing.Optional[jsii.Number] = None,
    session: typing.Optional[jsii.Number] = None,
    total: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673029b1d2b3b7b9f6ba109a03b7a73f7f5c7bea38d170bac99e720941e9022c(
    *,
    adm_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    apns_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    baidu_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CampaignCustomMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CampaignEmailMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gcm_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    in_app_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CampaignInAppMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sms_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CampaignSmsMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bc34013a62c0edc5a6f214411224d49e050250647a3a82b79757fe56202b12(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    image_icon_url: typing.Optional[builtins.str] = None,
    image_small_icon_url: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    json_body: typing.Optional[builtins.str] = None,
    media_url: typing.Optional[builtins.str] = None,
    raw_content: typing.Optional[builtins.str] = None,
    silent_push: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    time_to_live: typing.Optional[jsii.Number] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f3a5a251a9e03a3edca9a530106a058940f030b6387c1c9bf5e5f178f57950(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a095a94fc2a3f5f02c4bee6a6379e008774c3379ff92ccc90d393056c433c86e(
    *,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bddb3dc8424c9ff4650617fab4a715388f3cbc41ddc77bd8d174a6bdafbdfc1(
    *,
    end: builtins.str,
    start: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28328c02ca2d5803d7b94a649e1731518fd6571b2a3d476f0d52b1eaab811cd(
    *,
    end_time: typing.Optional[builtins.str] = None,
    event_filter: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CampaignEventFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    frequency: typing.Optional[builtins.str] = None,
    is_local_time: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    quiet_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_time: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62820699c46cf6118cb37ad264ac6bd74634ff8ac16df06981f6fda8bb10c8b1(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff680b114ac7eb3301e3ca9e3c054a07877c14dcee79f62b145a3323d877f717(
    *,
    email_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    push_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sms_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    voice_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51544243cac2e8deda2d5e6e42909b0810bb720b60bf05558129962396b6c511(
    *,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c287844519a3aec1773ace90dda6f6b00bb3d979c7b90db154d5f19df47bad(
    *,
    custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    message_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    size_percent: typing.Optional[jsii.Number] = None,
    template_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    treatment_description: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72587bc97db9489b7ff009b5e7e21b8672dd9834015792a5f49f1aa6e2de2b28(
    *,
    application_id: builtins.str,
    name: builtins.str,
    schedule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]],
    segment_id: builtins.str,
    additional_treatments: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.WriteTreatmentResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    campaign_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    holdout_percent: typing.Optional[jsii.Number] = None,
    is_paused: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    limits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.LimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    message_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    segment_version: typing.Optional[jsii.Number] = None,
    tags: typing.Any = None,
    template_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    treatment_description: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45ef6803da11b29d92a1a9dedc966b47a1d2605b1fe5fccb5246dddfc35974a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    from_address: builtins.str,
    identity: builtins.str,
    configuration_set: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba9980f2fd74da06e1ebc3614726e1c5828c881d5f32ab71fac8739256ea8c5(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3385e98cd386c8fd9b175addf07939f0a62ce826adf2dbbd5859a22437ec589(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4912ef26d0f430c81d117a5f0738e505c5c297269d1a30e2f2ebaadf888bc117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca335db0b8dfb92d4f3709cdefa228f99201c3be5f276ea0c1b91c43f2cfcf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b0d7f51338958e8b630f2bab7314510884f2d03614c934c994658b597484a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e401391c80933a2a367be2a6d52f36eece68b65d9cc1818ec569032f8db86e95(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5e325a8ba69d47d97054b07e5f37d86b62f5fc9a793b19194d843900f702ce(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec25179e4b582e0ac18ca6169a6cce37f50940251294b550528449a9abacbcfa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cd2fd919777b8e7d3ac652f2b80d489a8fa271bc155e3f51e0609aec57178e(
    *,
    application_id: builtins.str,
    from_address: builtins.str,
    identity: builtins.str,
    configuration_set: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d874cd34a09cafe787407bcc46d4f2da25256379f0805d9b3277c78cf3a6ce7d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    subject: builtins.str,
    template_name: builtins.str,
    default_substitutions: typing.Optional[builtins.str] = None,
    html_part: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
    text_part: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4845bb424606d811a5345c7d19273d48e2530fde2429a0b75c2de4451f2fe01d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d26377f4991209d1040e8926b3268c77351920f64e91dcc7a8ee07bea65361(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ee602488855db74e55d0725ce9ccd5dcaf5afb7f9041fafb2a3f004cc023a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337414baf14212153d471a735df91b0b208b8e21f9a3af27ed8d45d4b33a256f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e725be82af784b9ad6a1f9c3380b3bd506f34418ddce549dec83efb2eda43c0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96c5c7e2db544e6643fabe3a87b0849b9b5bfb84fd13605b99d18d53b8ec0ab(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa0217316fb53d9c6411e9537d3910fb71d255ee4e4b5bf5a133a3388b54472(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f43e87c31e4b4763bde93f0882c2fcaa98ebe283dee9aeb6c4de1c92a68b09(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ed26d7b8ff22bf96e4992ec66fa6f8f4f0a96e8dc7d62cfbe64407c8ad293a(
    *,
    subject: builtins.str,
    template_name: builtins.str,
    default_substitutions: typing.Optional[builtins.str] = None,
    html_part: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
    text_part: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be03b3b08c645b2ad088545ed60becc2d502a22d37e02777bb921d0c4359349(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    destination_stream_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8094e769a5b01a2b647af323a98530df95848e983909ad98fd70769294a342eb(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65223bde3aa70f7290d5d29057c7fc736f1f73560d2ff8478c0c1e4dfc5e999e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b72a36d4dbe0f60f071d9d942bfb6de4e856a7c430f57175604abaef6219a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b623a340671fc74c6884cc8202757c872bd3257d4604b29a217712eae288de90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc07fa45109777e615e00fbd7316434ce79f2ac50097d2ac51d5d666ae068c94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdb6b683e1b3c8b0ac5e4a9cbb95477d4817191bf0ad969320e26b97ee46b06(
    *,
    application_id: builtins.str,
    destination_stream_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9eaed45ea8e982f4384e74c9bb6d58e2bb50ab71b81ec8eb9663834eb40f68(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    api_key: builtins.str,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee2520c4272e766ba0a4239c563996907ec8d82983b8607a06d8c97c3f54f2c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8a9d9b2d9710aff98ca425ef3c722efadd68d8f9375e71c4e53100ed902c60(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe18164e431a229dfe4f3ed6e8be1938713396f5bc4716314cb650fc5c2ae14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ffd241afdcfa2aaf15677fee87435e32a5181cbbc3c5c41110b35f6e8fadbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307c8de02e27724c405c014f9dd6a91edb3c2ccf9dd15c311a610f1fd53b97f8(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799575c91c7b790ecebe50a1f908591fa3d7d3754d560c5f8051e43307513e57(
    *,
    api_key: builtins.str,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a58375e3084247c0cd1a4551d9a749b021dbad12e66dc0d65d7097eeb389a0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    template_name: builtins.str,
    content: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_config: typing.Any = None,
    layout: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa623197ed8dfdd5b6ea077a1267564e38ed76cde7a3f481fcda475c5fd3b44(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4100f78394daa226aff89f00d55dec1b35182e9d1582823bf3a6c1684ec5f2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0f5b30324249dbcf7967883532e48ac34155fc6a825e970ce7caa894e09229(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c54c1db617edfaec2d1880df4f13dd162442c1cad515fa6ada8b050e5cdf50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278ac4934402735235bea728305420ef61f4374ceca39785b68d3ab9024dd011(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInAppTemplate.InAppMessageContentProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd98e575ebe4e3646735d441e76df71a700ae5750834bd3fe9efea0bb3f8d6d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea20c5d2a069fd71769a2945612fa3a4466fef3a6c3ca5d82dbc959098901f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d89b51b3c0403b7d96e89a3d4ddd4537a1fa88688411aaf0eaf90733bcf98e0(
    *,
    alignment: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfbd704c6147b782ea69635d057627ac5ca2b9a14e9ed9df555a39a159d97c9(
    *,
    android: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.DefaultButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ios: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf7eb85b29234b3c2fea6fe8ac046f242a6f8637d3e8cb84baf14ee553046c0(
    *,
    background_color: typing.Optional[builtins.str] = None,
    border_radius: typing.Optional[jsii.Number] = None,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7d7f00dba390851da4a74e15f2cbfba584ff0c3dcfd02c79057d3e495a8426(
    *,
    alignment: typing.Optional[builtins.str] = None,
    header: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ad4b85282ac1d2a8384b4d73f0ea53928263965bc0416ac9676a6e6dc68ab6(
    *,
    background_color: typing.Optional[builtins.str] = None,
    body_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.BodyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    header_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.HeaderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_url: typing.Optional[builtins.str] = None,
    primary_btn: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.ButtonConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secondary_btn: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.ButtonConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07dcbc742cada193c5c4b997d8176916ddf68dcc52fd8cb5f229362873c40ec4(
    *,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d93034b4533bd842d7be555c9eef0012056db058958d6e0180cd8b62e90620b(
    *,
    template_name: builtins.str,
    content: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInAppTemplate.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_config: typing.Any = None,
    layout: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e234330089d446d7f323e4c73f1d9c1c17acc0e0e30d28c97d54c37c7c4a76e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    template_name: builtins.str,
    adm: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    apns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    baidu: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_substitutions: typing.Optional[builtins.str] = None,
    gcm: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69fca92e478053d0cc44916fbd64e74a2cb6e71987f1f78cd6f6dc1d560f3c1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1368e70eaee432841f8a64dd25110474cab976d2646e829941e7dd0026b49aaf(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733a68483e3bb9f727ebd95cdd0c0c723459549bfff847d29285135a1dc73c3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3e0bfcf687191128b7b58605ea3ecd33d73aeee2ce7892a26c98f627ddba49(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e2be7f43670056e7a6d731558fa33e8cf4475c8540b11898df56b3140d9ec9(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.APNSPushNotificationTemplateProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169b7f0cdb9b4fd53c5a7349f078aff8f1b19f6fad401e78c6e0669fa2a1b01c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520329f747f3fe8b8d0fd51174dae9ab0a39a0f6cbe587a14b80cad8f1d3a871(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.DefaultPushNotificationTemplateProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267ffcf4c6fca6192a102836f31a68c1a2ef0fc2b356b8df2374ba24a679ac76(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878bb27810504a86ab7ea470a0e25a1c91ca228c671844b097b4ba0125c444d5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPushTemplate.AndroidPushNotificationTemplateProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7291a982a472e0124687c43898c55ff61676c9c406522250462b9c8a234efb7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb0a399816d80399f7992f464408e5a015c38f3887194c0a8ec7fc67e726678(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    media_url: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f866be8e13a626d05404b7f7c753cce31f96ee49c91fb4e9328cd1e1ff25e66(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    image_icon_url: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    small_image_icon_url: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c71269ade76af4dae966ba08f6aa0718ac78505a335761ef4f79a8955a35fa(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444f4f10de75d3627ca6a158b3d14a85658b8f8d43cf6e0ff75307e722782866(
    *,
    template_name: builtins.str,
    adm: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    apns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    baidu: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_substitutions: typing.Optional[builtins.str] = None,
    gcm: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247e0e5db6df3760ce5285f312696c0525a8122dab3a894fc9e420f45b608f5e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    sender_id: typing.Optional[builtins.str] = None,
    short_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5eddd6bebc84e2365315fd2909a8d2a359e9c879be4ad3b8fb696c82861e9ed(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1499f7e636fe54076eb88578edbc4d2d332ca41d00d40e34d42ae56c780783cb(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979edcd25a20504bee120865d3c675d946146871879017a777fb6466da3cc52e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690b91b19b5fb26df4cd2a5740ffa6004a6a6f66aad08a1dd7cea96e210cd237(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a965e648aedad26bca950f0ef0214b33d05f0acd6812182eb6b2f4c0cf2896(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd359def565ce7c57596d41d3957b09dfa4a8d5b03403b031c18e654739247c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931b6acba9303ee19a2283bc8a621a4eefb65d2b2880b2ef0ffbb1467a2996eb(
    *,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    sender_id: typing.Optional[builtins.str] = None,
    short_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc023e804159f2b7b3b0630adc967114ee69038688e93e460806bebbcd49abd(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    name: builtins.str,
    dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    segment_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SegmentGroupsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7365726c90040db7625826a2214e0e44dc196900ff6edeb46c088ea26bbca5a4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f392d88b193fdce847c6174f5ce8112cca1b45b84d5109a4b4c63735f9cd9e4b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0a8e1574ac5acde84da0f41e348c6e9d69019ecdea8a1211569fbe942d6916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ee366eaedd5d0b9cd71b45cdb646586561f77c8a288dfec57bb418a8361cbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb90f1653a3ccc9627597904756a80e4c93e27a5f84a85544f921e1b9936ef5b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSegment.SegmentDimensionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf01cd98986d7b32e2d5189028538efed8d515cab1c84c5bce2ebc7c5c12923a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSegment.SegmentGroupsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e1a3df206fc6996c714f281147d93537936eb6c07c697d3fec6d1fabed0c14(
    *,
    attribute_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eec04bc94fd19713678447dbc443534c19776a0279e89e9c033e829a1e6f6a8(
    *,
    recency: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.RecencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4ec94323fbf3593aadcece503e2d7e202effa77c20d958789c0b45aca80678(
    *,
    latitude: jsii.Number,
    longitude: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c02d0e32ebdbe792d8ac0c08756a24a44927af6aa8185756c3a14f1a618d235(
    *,
    app_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    channel: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    device_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    make: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    model: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    platform: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1008e78bcf6ae7076bdcee0fa4c0d6db3875241ca67f0b48ccd700fd925c33(
    *,
    coordinates: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.CoordinatesProperty, typing.Dict[builtins.str, typing.Any]]],
    range_in_kilometers: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e2814269a21f322e99c218a52c06bd34848cb6fd92554e63f0acd87cead2e4(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_segments: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SourceSegmentsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03da39b2fc02da543c928064697aa37ea085d1266b04bb92464482904a073b6c(
    *,
    country: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gps_point: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.GPSPointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed252f3a3e8528df90cd7c6e4598509ad62fc1d1abb326877aed598872a04f1(
    *,
    duration: builtins.str,
    recency_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d312738042a72923349fd29b0e94bd1d8150a918330ada6380b5eed0ffff9b00(
    *,
    attributes: typing.Any = None,
    behavior: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.BehaviorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    demographic: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.DemographicProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Any = None,
    user_attributes: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42e1c0aa74d6e146120b91e8c3e5a61594133291e67f4772127e226ed7e8478(
    *,
    groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.GroupsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29af47784f33f34fc467d78482e24361671a1ceeded8ab66e7e8d21e1031f8f0(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd74be6bcbf3ee8ca9a4faf45de34d975ca0a33ef9d6cbd4bd1b0a8558104cb(
    *,
    id: builtins.str,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d585e38801e9b6deff4ac553d1071c24b8dda1e50267a4f728e0526c1b56f47(
    *,
    application_id: builtins.str,
    name: builtins.str,
    dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    segment_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSegment.SegmentGroupsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045e711f6ffe3f80379408f380b368a8b20279c46fafa222266842b600a2bd7d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    body: builtins.str,
    template_name: builtins.str,
    default_substitutions: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743ac17eb423e4f82cf1a8753bdc59bf131f0b00832b4b8ca27fcff976b64423(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8f6881df5a9d9b4389595d39af93a26548dd82a35626d4e6069818603d4d71(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf4352a92db77d953227e7523aefbc0fd61fc2b53806b5d9033aa1d11a0ccf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079b700c5a8d10acb8e7fe17a8d99e3584d3b67b84055e178278fe95dd000792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fbc34e4ef91f94707b3b93c20827ecbe498ee695470a70a92e3ae12db3833d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0195246c72c42c437f2f81a73dda3b8844c00948a5d4e418bd184ccba381bb17(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e77c53201ce08e15813d7f687acc3aa4a18801d783ec3d0f0455b8429c17828(
    *,
    body: builtins.str,
    template_name: builtins.str,
    default_substitutions: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1749026481cd71ef82009ec72de8b742285669d58162253b782b25af040107d8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4144c17931e8ba753cceec21e16fb551e637f7972ad3c90d7878c0db5409c692(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e091058e96733c9d30618a2df15e339da29c39292f62111e207083da8bef9363(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d770a12affe72d165755a98a2eb69adda9ed75395c551965177164023006922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa629f76a0d979c8a6cb0751e8bd5153c8fbcc8faa5fcafdc7d7a9230b74e917(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dbb601524c56bff5fa26ae1812175c95bcc222257fdfceab8fca30efeb1bf2d(
    *,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
