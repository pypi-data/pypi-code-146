'''
# `datadog_cloud_configuration_rule`

Refer to the Terraform Registory for docs: [`datadog_cloud_configuration_rule`](https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule).
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class CloudConfigurationRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.cloudConfigurationRule.CloudConfigurationRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule datadog_cloud_configuration_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        message: builtins.str,
        name: builtins.str,
        policy: builtins.str,
        resource_type: builtins.str,
        severity: builtins.str,
        group_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        related_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule datadog_cloud_configuration_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Whether the cloud configuration rule is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#enabled CloudConfigurationRule#enabled}
        :param message: The message associated to the rule that will be shown in findings and signals. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#message CloudConfigurationRule#message}
        :param name: The name of the cloud configuration rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#name CloudConfigurationRule#name}
        :param policy: Policy written in Rego format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#policy CloudConfigurationRule#policy}
        :param resource_type: Main resource type to be checked by the rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#resource_type CloudConfigurationRule#resource_type}
        :param severity: Severity of the rule and associated signals. Valid values are ``info``, ``low``, ``medium``, ``high``, ``critical``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#severity CloudConfigurationRule#severity}
        :param group_by: Fields to group by when generating signals, e.g. @resource. Defaults to empty list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#group_by CloudConfigurationRule#group_by}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#id CloudConfigurationRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notifications: Notification targets for signals. Defaults to empty list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#notifications CloudConfigurationRule#notifications}
        :param related_resource_types: Related resource types to be checked by the rule. Defaults to empty list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#related_resource_types CloudConfigurationRule#related_resource_types}
        :param tags: Tags of the rule, propagated to findings and signals. Defaults to empty list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#tags CloudConfigurationRule#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd4a375aee9700a1912f6b982112111616b22ad885c0c179f25446706d8985b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudConfigurationRuleConfig(
            enabled=enabled,
            message=message,
            name=name,
            policy=policy,
            resource_type=resource_type,
            severity=severity,
            group_by=group_by,
            id=id,
            notifications=notifications,
            related_resource_types=related_resource_types,
            tags=tags,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetGroupBy")
    def reset_group_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupBy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotifications")
    def reset_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifications", []))

    @jsii.member(jsii_name="resetRelatedResourceTypes")
    def reset_related_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelatedResourceTypes", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByInput")
    def group_by_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupByInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationsInput")
    def notifications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="relatedResourceTypesInput")
    def related_resource_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "relatedResourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98fd20e9cfdf85e7dcbc4f1efa35aa5f7c8c8afab81f79e5ca03fddd57c432c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="groupBy")
    def group_by(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupBy"))

    @group_by.setter
    def group_by(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c51dad0709b915cf49b4609667734b893b5675981076278470a4d15bb5ae3c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupBy", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3742a76ee862a26f8d39229e03cf76a0e86fc8b94e310ca1d525478307ddd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091435c9261a45f35ad58598a51cd62f14b293e66ff5cafbae2a56a724b0cfa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f9f1f55e60b4a4057ced1732f6b0ad0aa570401c746c7b50e7159b47c67306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="notifications")
    def notifications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifications"))

    @notifications.setter
    def notifications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bccbde665dba557b1079db447d134f411820d967565fd6e4c7937dfcf6546089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifications", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe530b2f54a8246ae7b0c9302e84d2ec73dadf54b0c543aea33dcdf2395996d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="relatedResourceTypes")
    def related_resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "relatedResourceTypes"))

    @related_resource_types.setter
    def related_resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd4a40d9461a25d16cd986d72ba42cb41eb393a78724a07972efed73812ada5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relatedResourceTypes", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0360b4ef7f64fb1e8239e3c32f7c9cf0edcb054f604448d9c354ac32a1d2801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68caa94824dd99261282e79e463cff59f1ec9616edc6e36d3aaeed3e59848ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e675337328593fdca5bfb760f1d53ebf9be1cc0763c1aa58f6fea667305b9389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.cloudConfigurationRule.CloudConfigurationRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enabled": "enabled",
        "message": "message",
        "name": "name",
        "policy": "policy",
        "resource_type": "resourceType",
        "severity": "severity",
        "group_by": "groupBy",
        "id": "id",
        "notifications": "notifications",
        "related_resource_types": "relatedResourceTypes",
        "tags": "tags",
    },
)
class CloudConfigurationRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        message: builtins.str,
        name: builtins.str,
        policy: builtins.str,
        resource_type: builtins.str,
        severity: builtins.str,
        group_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        related_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enabled: Whether the cloud configuration rule is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#enabled CloudConfigurationRule#enabled}
        :param message: The message associated to the rule that will be shown in findings and signals. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#message CloudConfigurationRule#message}
        :param name: The name of the cloud configuration rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#name CloudConfigurationRule#name}
        :param policy: Policy written in Rego format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#policy CloudConfigurationRule#policy}
        :param resource_type: Main resource type to be checked by the rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#resource_type CloudConfigurationRule#resource_type}
        :param severity: Severity of the rule and associated signals. Valid values are ``info``, ``low``, ``medium``, ``high``, ``critical``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#severity CloudConfigurationRule#severity}
        :param group_by: Fields to group by when generating signals, e.g. @resource. Defaults to empty list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#group_by CloudConfigurationRule#group_by}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#id CloudConfigurationRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notifications: Notification targets for signals. Defaults to empty list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#notifications CloudConfigurationRule#notifications}
        :param related_resource_types: Related resource types to be checked by the rule. Defaults to empty list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#related_resource_types CloudConfigurationRule#related_resource_types}
        :param tags: Tags of the rule, propagated to findings and signals. Defaults to empty list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#tags CloudConfigurationRule#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79dea7209050f2743470c102fda9bee26f53b76305716e98f0d708308d92f88)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument group_by", value=group_by, expected_type=type_hints["group_by"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
            check_type(argname="argument related_resource_types", value=related_resource_types, expected_type=type_hints["related_resource_types"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "message": message,
            "name": name,
            "policy": policy,
            "resource_type": resource_type,
            "severity": severity,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if group_by is not None:
            self._values["group_by"] = group_by
        if id is not None:
            self._values["id"] = id
        if notifications is not None:
            self._values["notifications"] = notifications
        if related_resource_types is not None:
            self._values["related_resource_types"] = related_resource_types
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the cloud configuration rule is enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#enabled CloudConfigurationRule#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def message(self) -> builtins.str:
        '''The message associated to the rule that will be shown in findings and signals.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#message CloudConfigurationRule#message}
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the cloud configuration rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#name CloudConfigurationRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy(self) -> builtins.str:
        '''Policy written in Rego format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#policy CloudConfigurationRule#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''Main resource type to be checked by the rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#resource_type CloudConfigurationRule#resource_type}
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''Severity of the rule and associated signals. Valid values are ``info``, ``low``, ``medium``, ``high``, ``critical``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#severity CloudConfigurationRule#severity}
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_by(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fields to group by when generating signals, e.g. @resource. Defaults to empty list.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#group_by CloudConfigurationRule#group_by}
        '''
        result = self._values.get("group_by")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#id CloudConfigurationRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Notification targets for signals. Defaults to empty list.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#notifications CloudConfigurationRule#notifications}
        '''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def related_resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Related resource types to be checked by the rule. Defaults to empty list.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#related_resource_types CloudConfigurationRule#related_resource_types}
        '''
        result = self._values.get("related_resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags of the rule, propagated to findings and signals. Defaults to empty list.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/cloud_configuration_rule#tags CloudConfigurationRule#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudConfigurationRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudConfigurationRule",
    "CloudConfigurationRuleConfig",
]

publication.publish()

def _typecheckingstub__ccd4a375aee9700a1912f6b982112111616b22ad885c0c179f25446706d8985b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    message: builtins.str,
    name: builtins.str,
    policy: builtins.str,
    resource_type: builtins.str,
    severity: builtins.str,
    group_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
    related_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98fd20e9cfdf85e7dcbc4f1efa35aa5f7c8c8afab81f79e5ca03fddd57c432c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c51dad0709b915cf49b4609667734b893b5675981076278470a4d15bb5ae3c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3742a76ee862a26f8d39229e03cf76a0e86fc8b94e310ca1d525478307ddd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091435c9261a45f35ad58598a51cd62f14b293e66ff5cafbae2a56a724b0cfa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f9f1f55e60b4a4057ced1732f6b0ad0aa570401c746c7b50e7159b47c67306(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bccbde665dba557b1079db447d134f411820d967565fd6e4c7937dfcf6546089(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe530b2f54a8246ae7b0c9302e84d2ec73dadf54b0c543aea33dcdf2395996d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd4a40d9461a25d16cd986d72ba42cb41eb393a78724a07972efed73812ada5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0360b4ef7f64fb1e8239e3c32f7c9cf0edcb054f604448d9c354ac32a1d2801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68caa94824dd99261282e79e463cff59f1ec9616edc6e36d3aaeed3e59848ae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e675337328593fdca5bfb760f1d53ebf9be1cc0763c1aa58f6fea667305b9389(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79dea7209050f2743470c102fda9bee26f53b76305716e98f0d708308d92f88(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    message: builtins.str,
    name: builtins.str,
    policy: builtins.str,
    resource_type: builtins.str,
    severity: builtins.str,
    group_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
    related_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
