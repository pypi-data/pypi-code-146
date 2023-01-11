'''
# AWS::SupportApp Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as supportapp
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for SupportApp construct libraries](https://constructs.dev/search?q=supportapp)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::SupportApp resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SupportApp.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::SupportApp](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SupportApp.html).

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
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAccountAlias(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_supportapp.CfnAccountAlias",
):
    '''A CloudFormation ``AWS::SupportApp::AccountAlias``.

    You can use the ``AWS::SupportApp::AccountAlias`` resource to specify your AWS account when you configure the AWS Support App in Slack. Your alias name appears on the AWS Support App page in the Support Center Console and in messages from the AWS Support App. You can use this alias to identify the account you've configured with the AWS Support App .

    For more information, see `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_ in the *AWS Support User Guide* .

    :cloudformationResource: AWS::SupportApp::AccountAlias
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_supportapp as supportapp
        
        cfn_account_alias = supportapp.CfnAccountAlias(self, "MyCfnAccountAlias",
            account_alias="accountAlias"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        account_alias: builtins.str,
    ) -> None:
        '''Create a new ``AWS::SupportApp::AccountAlias``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_alias: An alias or short name for an AWS account .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d67fabe6ef269f1fea9a73a8372a4ff9dc5378592b63a14c7d79b827ef4301)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccountAliasProps(account_alias=account_alias)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225c3075103e21bd15099769a972551ff3c0baf7f15556f11f064f4effa9102b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f68b95ae735930b73f6c33b21c4be9a30270f2acddf2adfce521c8de14bfe8a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountAliasResourceId")
    def attr_account_alias_resource_id(self) -> builtins.str:
        '''The ``AccountAlias`` resource type has an attribute ``AccountAliasResourceId`` . You can use this attribute to identify the resource.

        The ``AccountAliasResourceId`` will be ``AccountAlias_for_accountId`` . In this example, ``AccountAlias_for_`` is the prefix and ``accountId`` is your AWS account number, such as ``AccountAlias_for_123456789012`` .

        :cloudformationAttribute: AccountAliasResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccountAliasResourceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="accountAlias")
    def account_alias(self) -> builtins.str:
        '''An alias or short name for an AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html#cfn-supportapp-accountalias-accountalias
        '''
        return typing.cast(builtins.str, jsii.get(self, "accountAlias"))

    @account_alias.setter
    def account_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a3f2b686ca5bda799e5d951585c1d7cf54d2e06aea95017e2c6547322b7970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountAlias", value)


@jsii.data_type(
    jsii_type="monocdk.aws_supportapp.CfnAccountAliasProps",
    jsii_struct_bases=[],
    name_mapping={"account_alias": "accountAlias"},
)
class CfnAccountAliasProps:
    def __init__(self, *, account_alias: builtins.str) -> None:
        '''Properties for defining a ``CfnAccountAlias``.

        :param account_alias: An alias or short name for an AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_supportapp as supportapp
            
            cfn_account_alias_props = supportapp.CfnAccountAliasProps(
                account_alias="accountAlias"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229e919e1087d1c21d29edd92e11f75d6fc95fcd34843835cde68f69fd5ab8d3)
            check_type(argname="argument account_alias", value=account_alias, expected_type=type_hints["account_alias"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_alias": account_alias,
        }

    @builtins.property
    def account_alias(self) -> builtins.str:
        '''An alias or short name for an AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html#cfn-supportapp-accountalias-accountalias
        '''
        result = self._values.get("account_alias")
        assert result is not None, "Required property 'account_alias' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccountAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSlackChannelConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_supportapp.CfnSlackChannelConfiguration",
):
    '''A CloudFormation ``AWS::SupportApp::SlackChannelConfiguration``.

    You can use the ``AWS::SupportApp::SlackChannelConfiguration`` resource to specify your AWS account when you configure the AWS Support App . This resource includes the following information:

    - The Slack channel name and ID
    - The team ID in Slack
    - The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role
    - Whether you want the AWS Support App to notify you when your support cases are created, updated, resolved, or reopened
    - The case severity that you want to get notified for

    For more information, see the following topics in the *AWS Support User Guide* :

    - `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_
    - `Creating AWS Support App in Slack resources with AWS CloudFormation <https://docs.aws.amazon.com/awssupport/latest/user/creating-resources-with-cloudformation.html>`_

    :cloudformationResource: AWS::SupportApp::SlackChannelConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_supportapp as supportapp
        
        cfn_slack_channel_configuration = supportapp.CfnSlackChannelConfiguration(self, "MyCfnSlackChannelConfiguration",
            channel_id="channelId",
            channel_role_arn="channelRoleArn",
            notify_on_case_severity="notifyOnCaseSeverity",
            team_id="teamId",
        
            # the properties below are optional
            channel_name="channelName",
            notify_on_add_correspondence_to_case=False,
            notify_on_create_or_reopen_case=False,
            notify_on_resolve_case=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        channel_id: builtins.str,
        channel_role_arn: builtins.str,
        notify_on_case_severity: builtins.str,
        team_id: builtins.str,
        channel_name: typing.Optional[builtins.str] = None,
        notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::SupportApp::SlackChannelConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel_id: The channel ID in Slack. This ID identifies a channel within a Slack workspace.
        :param channel_role_arn: The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration. The AWS Support App uses this role to perform AWS Support and Service Quotas actions on your behalf.
        :param notify_on_case_severity: The case severity for your support cases that you want to receive notifications. You can specify ``none`` , ``all`` , or ``high`` .
        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace.
        :param channel_name: The channel name in Slack. This is the channel where you invite the AWS Support App .
        :param notify_on_add_correspondence_to_case: Whether to get notified when a correspondence is added to your support cases.
        :param notify_on_create_or_reopen_case: Whether to get notified when your support cases are created or reopened.
        :param notify_on_resolve_case: Whether to get notified when your support cases are resolved.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbcc378c416e76108283303827dd8434468dff1e51c09d911f33eba080b0dd81)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSlackChannelConfigurationProps(
            channel_id=channel_id,
            channel_role_arn=channel_role_arn,
            notify_on_case_severity=notify_on_case_severity,
            team_id=team_id,
            channel_name=channel_name,
            notify_on_add_correspondence_to_case=notify_on_add_correspondence_to_case,
            notify_on_create_or_reopen_case=notify_on_create_or_reopen_case,
            notify_on_resolve_case=notify_on_resolve_case,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbacc33c51154ef8e4dbcb46ef7d6ed6be88f77e8c9978536b40ff09bd1ebac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6aa121f8958e40ba455046a2fe2918b1c051bd254d553a432ec9cda2e29829b)
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
    @jsii.member(jsii_name="channelId")
    def channel_id(self) -> builtins.str:
        '''The channel ID in Slack.

        This ID identifies a channel within a Slack workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelid
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelId"))

    @channel_id.setter
    def channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ad4528a4fed6b8509d2c8341555c1ce34208d1ef9ff6a6adb9ce7d563d5a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelId", value)

    @builtins.property
    @jsii.member(jsii_name="channelRoleArn")
    def channel_role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration.

        The AWS Support App uses this role to perform AWS Support and Service Quotas actions on your behalf.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelRoleArn"))

    @channel_role_arn.setter
    def channel_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b63adf47f5ad2a8b1cd10d34d3eed3270413f64fdc3f5015580dbd434868af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="notifyOnCaseSeverity")
    def notify_on_case_severity(self) -> builtins.str:
        '''The case severity for your support cases that you want to receive notifications.

        You can specify ``none`` , ``all`` , or ``high`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncaseseverity
        '''
        return typing.cast(builtins.str, jsii.get(self, "notifyOnCaseSeverity"))

    @notify_on_case_severity.setter
    def notify_on_case_severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a63f7d7a82a61dfc7a1eeb0c80e4392e4e7931a673b18722a9003c12dcce178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnCaseSeverity", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-teamid
        '''
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78368f171665f70f3b52a5e8558d93a50407201bf3252d6e4bb15448c0b7ccc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The channel name in Slack.

        This is the channel where you invite the AWS Support App .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9006c4ff4830922d68505336afe29da7ae48c1295e99839c2980b4b4eb182d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value)

    @builtins.property
    @jsii.member(jsii_name="notifyOnAddCorrespondenceToCase")
    def notify_on_add_correspondence_to_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to get notified when a correspondence is added to your support cases.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonaddcorrespondencetocase
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "notifyOnAddCorrespondenceToCase"))

    @notify_on_add_correspondence_to_case.setter
    def notify_on_add_correspondence_to_case(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971a76c8124884260cbf50dd8a79beb35b95ea5ff718e05300418461dee44fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnAddCorrespondenceToCase", value)

    @builtins.property
    @jsii.member(jsii_name="notifyOnCreateOrReopenCase")
    def notify_on_create_or_reopen_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to get notified when your support cases are created or reopened.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncreateorreopencase
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "notifyOnCreateOrReopenCase"))

    @notify_on_create_or_reopen_case.setter
    def notify_on_create_or_reopen_case(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cfb9a4db0e46a7ce9a1a4428a9187706f5f541856d9c158482cb6dea030ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnCreateOrReopenCase", value)

    @builtins.property
    @jsii.member(jsii_name="notifyOnResolveCase")
    def notify_on_resolve_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to get notified when your support cases are resolved.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonresolvecase
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "notifyOnResolveCase"))

    @notify_on_resolve_case.setter
    def notify_on_resolve_case(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b484fdd66dfd744da0e3f2c5f1e47a8957ffab8c05e3a8f991db64b31e99b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnResolveCase", value)


@jsii.data_type(
    jsii_type="monocdk.aws_supportapp.CfnSlackChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_id": "channelId",
        "channel_role_arn": "channelRoleArn",
        "notify_on_case_severity": "notifyOnCaseSeverity",
        "team_id": "teamId",
        "channel_name": "channelName",
        "notify_on_add_correspondence_to_case": "notifyOnAddCorrespondenceToCase",
        "notify_on_create_or_reopen_case": "notifyOnCreateOrReopenCase",
        "notify_on_resolve_case": "notifyOnResolveCase",
    },
)
class CfnSlackChannelConfigurationProps:
    def __init__(
        self,
        *,
        channel_id: builtins.str,
        channel_role_arn: builtins.str,
        notify_on_case_severity: builtins.str,
        team_id: builtins.str,
        channel_name: typing.Optional[builtins.str] = None,
        notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSlackChannelConfiguration``.

        :param channel_id: The channel ID in Slack. This ID identifies a channel within a Slack workspace.
        :param channel_role_arn: The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration. The AWS Support App uses this role to perform AWS Support and Service Quotas actions on your behalf.
        :param notify_on_case_severity: The case severity for your support cases that you want to receive notifications. You can specify ``none`` , ``all`` , or ``high`` .
        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace.
        :param channel_name: The channel name in Slack. This is the channel where you invite the AWS Support App .
        :param notify_on_add_correspondence_to_case: Whether to get notified when a correspondence is added to your support cases.
        :param notify_on_create_or_reopen_case: Whether to get notified when your support cases are created or reopened.
        :param notify_on_resolve_case: Whether to get notified when your support cases are resolved.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_supportapp as supportapp
            
            cfn_slack_channel_configuration_props = supportapp.CfnSlackChannelConfigurationProps(
                channel_id="channelId",
                channel_role_arn="channelRoleArn",
                notify_on_case_severity="notifyOnCaseSeverity",
                team_id="teamId",
            
                # the properties below are optional
                channel_name="channelName",
                notify_on_add_correspondence_to_case=False,
                notify_on_create_or_reopen_case=False,
                notify_on_resolve_case=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4735d1012ee9a802c287574d5830e50f8bd673add0aa4b642a8b62a805a7b4)
            check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
            check_type(argname="argument channel_role_arn", value=channel_role_arn, expected_type=type_hints["channel_role_arn"])
            check_type(argname="argument notify_on_case_severity", value=notify_on_case_severity, expected_type=type_hints["notify_on_case_severity"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument notify_on_add_correspondence_to_case", value=notify_on_add_correspondence_to_case, expected_type=type_hints["notify_on_add_correspondence_to_case"])
            check_type(argname="argument notify_on_create_or_reopen_case", value=notify_on_create_or_reopen_case, expected_type=type_hints["notify_on_create_or_reopen_case"])
            check_type(argname="argument notify_on_resolve_case", value=notify_on_resolve_case, expected_type=type_hints["notify_on_resolve_case"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_id": channel_id,
            "channel_role_arn": channel_role_arn,
            "notify_on_case_severity": notify_on_case_severity,
            "team_id": team_id,
        }
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if notify_on_add_correspondence_to_case is not None:
            self._values["notify_on_add_correspondence_to_case"] = notify_on_add_correspondence_to_case
        if notify_on_create_or_reopen_case is not None:
            self._values["notify_on_create_or_reopen_case"] = notify_on_create_or_reopen_case
        if notify_on_resolve_case is not None:
            self._values["notify_on_resolve_case"] = notify_on_resolve_case

    @builtins.property
    def channel_id(self) -> builtins.str:
        '''The channel ID in Slack.

        This ID identifies a channel within a Slack workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelid
        '''
        result = self._values.get("channel_id")
        assert result is not None, "Required property 'channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel_role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration.

        The AWS Support App uses this role to perform AWS Support and Service Quotas actions on your behalf.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelrolearn
        '''
        result = self._values.get("channel_role_arn")
        assert result is not None, "Required property 'channel_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notify_on_case_severity(self) -> builtins.str:
        '''The case severity for your support cases that you want to receive notifications.

        You can specify ``none`` , ``all`` , or ``high`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncaseseverity
        '''
        result = self._values.get("notify_on_case_severity")
        assert result is not None, "Required property 'notify_on_case_severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-teamid
        '''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The channel name in Slack.

        This is the channel where you invite the AWS Support App .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notify_on_add_correspondence_to_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to get notified when a correspondence is added to your support cases.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonaddcorrespondencetocase
        '''
        result = self._values.get("notify_on_add_correspondence_to_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def notify_on_create_or_reopen_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to get notified when your support cases are created or reopened.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncreateorreopencase
        '''
        result = self._values.get("notify_on_create_or_reopen_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def notify_on_resolve_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to get notified when your support cases are resolved.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonresolvecase
        '''
        result = self._values.get("notify_on_resolve_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSlackWorkspaceConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_supportapp.CfnSlackWorkspaceConfiguration",
):
    '''A CloudFormation ``AWS::SupportApp::SlackWorkspaceConfiguration``.

    You can use the ``AWS::SupportApp::SlackWorkspaceConfiguration`` resource to specify your Slack workspace configuration. This resource configures your AWS account so that you can use the specified Slack workspace in the AWS Support App . This resource includes the following information:

    - The team ID for the Slack workspace
    - The version ID of the resource to use with AWS CloudFormation

    For more information, see the following topics in the *AWS Support User Guide* :

    - `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_
    - `Creating AWS Support App in Slack resources with AWS CloudFormation <https://docs.aws.amazon.com/awssupport/latest/user/creating-resources-with-cloudformation.html>`_

    :cloudformationResource: AWS::SupportApp::SlackWorkspaceConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_supportapp as supportapp
        
        cfn_slack_workspace_configuration = supportapp.CfnSlackWorkspaceConfiguration(self, "MyCfnSlackWorkspaceConfiguration",
            team_id="teamId",
        
            # the properties below are optional
            version_id="versionId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        team_id: builtins.str,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::SupportApp::SlackWorkspaceConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .
        :param version_id: An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2457cff2802c92973c4b9a9fb5f307107d0a11acfc7e5f56c13b0fc621ae3ad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSlackWorkspaceConfigurationProps(
            team_id=team_id, version_id=version_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcfe70d6421f904e1bc556318f88469c85bdb7e2697b5a853960d15099c7f88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04d0bd1759676da96beb545c8dfcfe692ed22fb1bb9e83c0fa49b7030185b56c)
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
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-teamid
        '''
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba7f8b35360f602a1fb10b147e8a2089a5d34689c6b1267c3bee4c5ea8f7e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> typing.Optional[builtins.str]:
        '''An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-versionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bcd48cf5be2e89c2d7bacee604248a88b059530c584ea565732e8b5acd1841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_supportapp.CfnSlackWorkspaceConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"team_id": "teamId", "version_id": "versionId"},
)
class CfnSlackWorkspaceConfigurationProps:
    def __init__(
        self,
        *,
        team_id: builtins.str,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSlackWorkspaceConfiguration``.

        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .
        :param version_id: An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_supportapp as supportapp
            
            cfn_slack_workspace_configuration_props = supportapp.CfnSlackWorkspaceConfigurationProps(
                team_id="teamId",
            
                # the properties below are optional
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4531955a3b9a8060c2e76e14389f2c3b774216f1edb1a2396c458a2887b45a)
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "team_id": team_id,
        }
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def team_id(self) -> builtins.str:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-teamid
        '''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackWorkspaceConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAccountAlias",
    "CfnAccountAliasProps",
    "CfnSlackChannelConfiguration",
    "CfnSlackChannelConfigurationProps",
    "CfnSlackWorkspaceConfiguration",
    "CfnSlackWorkspaceConfigurationProps",
]

publication.publish()

def _typecheckingstub__26d67fabe6ef269f1fea9a73a8372a4ff9dc5378592b63a14c7d79b827ef4301(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    account_alias: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225c3075103e21bd15099769a972551ff3c0baf7f15556f11f064f4effa9102b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f68b95ae735930b73f6c33b21c4be9a30270f2acddf2adfce521c8de14bfe8a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a3f2b686ca5bda799e5d951585c1d7cf54d2e06aea95017e2c6547322b7970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229e919e1087d1c21d29edd92e11f75d6fc95fcd34843835cde68f69fd5ab8d3(
    *,
    account_alias: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbcc378c416e76108283303827dd8434468dff1e51c09d911f33eba080b0dd81(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    channel_id: builtins.str,
    channel_role_arn: builtins.str,
    notify_on_case_severity: builtins.str,
    team_id: builtins.str,
    channel_name: typing.Optional[builtins.str] = None,
    notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbacc33c51154ef8e4dbcb46ef7d6ed6be88f77e8c9978536b40ff09bd1ebac(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6aa121f8958e40ba455046a2fe2918b1c051bd254d553a432ec9cda2e29829b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ad4528a4fed6b8509d2c8341555c1ce34208d1ef9ff6a6adb9ce7d563d5a6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b63adf47f5ad2a8b1cd10d34d3eed3270413f64fdc3f5015580dbd434868af3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a63f7d7a82a61dfc7a1eeb0c80e4392e4e7931a673b18722a9003c12dcce178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78368f171665f70f3b52a5e8558d93a50407201bf3252d6e4bb15448c0b7ccc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9006c4ff4830922d68505336afe29da7ae48c1295e99839c2980b4b4eb182d96(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971a76c8124884260cbf50dd8a79beb35b95ea5ff718e05300418461dee44fad(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cfb9a4db0e46a7ce9a1a4428a9187706f5f541856d9c158482cb6dea030ca5(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b484fdd66dfd744da0e3f2c5f1e47a8957ffab8c05e3a8f991db64b31e99b9(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4735d1012ee9a802c287574d5830e50f8bd673add0aa4b642a8b62a805a7b4(
    *,
    channel_id: builtins.str,
    channel_role_arn: builtins.str,
    notify_on_case_severity: builtins.str,
    team_id: builtins.str,
    channel_name: typing.Optional[builtins.str] = None,
    notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2457cff2802c92973c4b9a9fb5f307107d0a11acfc7e5f56c13b0fc621ae3ad(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    team_id: builtins.str,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcfe70d6421f904e1bc556318f88469c85bdb7e2697b5a853960d15099c7f88(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d0bd1759676da96beb545c8dfcfe692ed22fb1bb9e83c0fa49b7030185b56c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba7f8b35360f602a1fb10b147e8a2089a5d34689c6b1267c3bee4c5ea8f7e93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bcd48cf5be2e89c2d7bacee604248a88b059530c584ea565732e8b5acd1841(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4531955a3b9a8060c2e76e14389f2c3b774216f1edb1a2396c458a2887b45a(
    *,
    team_id: builtins.str,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
