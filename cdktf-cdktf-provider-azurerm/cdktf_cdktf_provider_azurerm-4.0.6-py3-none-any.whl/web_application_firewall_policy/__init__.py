'''
# `azurerm_web_application_firewall_policy`

Refer to the Terraform Registory for docs: [`azurerm_web_application_firewall_policy`](https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy).
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


class WebApplicationFirewallPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy azurerm_web_application_firewall_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        managed_rules: typing.Union["WebApplicationFirewallPolicyManagedRules", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        resource_group_name: builtins.str,
        custom_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyCustomRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        policy_settings: typing.Optional[typing.Union["WebApplicationFirewallPolicyPolicySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["WebApplicationFirewallPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy azurerm_web_application_firewall_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#location WebApplicationFirewallPolicy#location}.
        :param managed_rules: managed_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#managed_rules WebApplicationFirewallPolicy#managed_rules}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#name WebApplicationFirewallPolicy#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#resource_group_name WebApplicationFirewallPolicy#resource_group_name}.
        :param custom_rules: custom_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#custom_rules WebApplicationFirewallPolicy#custom_rules}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#id WebApplicationFirewallPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_settings: policy_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#policy_settings WebApplicationFirewallPolicy#policy_settings}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#tags WebApplicationFirewallPolicy#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#timeouts WebApplicationFirewallPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1011c6efdc5e09194917c9842844a514e10ed7f3cc1bf5d64300d10b4ccd31)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WebApplicationFirewallPolicyConfig(
            location=location,
            managed_rules=managed_rules,
            name=name,
            resource_group_name=resource_group_name,
            custom_rules=custom_rules,
            id=id,
            policy_settings=policy_settings,
            tags=tags,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCustomRules")
    def put_custom_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyCustomRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b3ba5b93c7d443377ec1979a61bb716a3631f7f4043448316103ce0398010f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomRules", [value]))

    @jsii.member(jsii_name="putManagedRules")
    def put_managed_rules(
        self,
        *,
        managed_rule_set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesManagedRuleSet", typing.Dict[builtins.str, typing.Any]]]],
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param managed_rule_set: managed_rule_set block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#managed_rule_set WebApplicationFirewallPolicy#managed_rule_set}
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#exclusion WebApplicationFirewallPolicy#exclusion}
        '''
        value = WebApplicationFirewallPolicyManagedRules(
            managed_rule_set=managed_rule_set, exclusion=exclusion
        )

        return typing.cast(None, jsii.invoke(self, "putManagedRules", [value]))

    @jsii.member(jsii_name="putPolicySettings")
    def put_policy_settings(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_upload_limit_in_mb: typing.Optional[jsii.Number] = None,
        max_request_body_size_in_kb: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
        request_body_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#enabled WebApplicationFirewallPolicy#enabled}.
        :param file_upload_limit_in_mb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#file_upload_limit_in_mb WebApplicationFirewallPolicy#file_upload_limit_in_mb}.
        :param max_request_body_size_in_kb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#max_request_body_size_in_kb WebApplicationFirewallPolicy#max_request_body_size_in_kb}.
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#mode WebApplicationFirewallPolicy#mode}.
        :param request_body_check: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#request_body_check WebApplicationFirewallPolicy#request_body_check}.
        '''
        value = WebApplicationFirewallPolicyPolicySettings(
            enabled=enabled,
            file_upload_limit_in_mb=file_upload_limit_in_mb,
            max_request_body_size_in_kb=max_request_body_size_in_kb,
            mode=mode,
            request_body_check=request_body_check,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicySettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#create WebApplicationFirewallPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#delete WebApplicationFirewallPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#read WebApplicationFirewallPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#update WebApplicationFirewallPolicy#update}.
        '''
        value = WebApplicationFirewallPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomRules")
    def reset_custom_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRules", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPolicySettings")
    def reset_policy_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicySettings", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="customRules")
    def custom_rules(self) -> "WebApplicationFirewallPolicyCustomRulesList":
        return typing.cast("WebApplicationFirewallPolicyCustomRulesList", jsii.get(self, "customRules"))

    @builtins.property
    @jsii.member(jsii_name="httpListenerIds")
    def http_listener_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpListenerIds"))

    @builtins.property
    @jsii.member(jsii_name="managedRules")
    def managed_rules(
        self,
    ) -> "WebApplicationFirewallPolicyManagedRulesOutputReference":
        return typing.cast("WebApplicationFirewallPolicyManagedRulesOutputReference", jsii.get(self, "managedRules"))

    @builtins.property
    @jsii.member(jsii_name="pathBasedRuleIds")
    def path_based_rule_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pathBasedRuleIds"))

    @builtins.property
    @jsii.member(jsii_name="policySettings")
    def policy_settings(
        self,
    ) -> "WebApplicationFirewallPolicyPolicySettingsOutputReference":
        return typing.cast("WebApplicationFirewallPolicyPolicySettingsOutputReference", jsii.get(self, "policySettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WebApplicationFirewallPolicyTimeoutsOutputReference":
        return typing.cast("WebApplicationFirewallPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="customRulesInput")
    def custom_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyCustomRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyCustomRules"]]], jsii.get(self, "customRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedRulesInput")
    def managed_rules_input(
        self,
    ) -> typing.Optional["WebApplicationFirewallPolicyManagedRules"]:
        return typing.cast(typing.Optional["WebApplicationFirewallPolicyManagedRules"], jsii.get(self, "managedRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policySettingsInput")
    def policy_settings_input(
        self,
    ) -> typing.Optional["WebApplicationFirewallPolicyPolicySettings"]:
        return typing.cast(typing.Optional["WebApplicationFirewallPolicyPolicySettings"], jsii.get(self, "policySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["WebApplicationFirewallPolicyTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["WebApplicationFirewallPolicyTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e287fc0aa7f9aca943799bee97133b366f1fca39d1acfa3dc28e462e94aefa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ffe5a05a5fea90affba48e7d91a5ad66a399ff58003324401ba2a84f597652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e275007680d9ba18e2b5c015ecf8d383e4bdd288ef280cc1c5240c316d3389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf3bc8e89a2fe42ee30cb3da287cce95217b95ba05f0b24650026931edb52e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e2229c572be7b31330f4059f72c8b582f4d8c7b197a176a357676514473a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "managed_rules": "managedRules",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "custom_rules": "customRules",
        "id": "id",
        "policy_settings": "policySettings",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class WebApplicationFirewallPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        managed_rules: typing.Union["WebApplicationFirewallPolicyManagedRules", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        resource_group_name: builtins.str,
        custom_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyCustomRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        policy_settings: typing.Optional[typing.Union["WebApplicationFirewallPolicyPolicySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["WebApplicationFirewallPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#location WebApplicationFirewallPolicy#location}.
        :param managed_rules: managed_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#managed_rules WebApplicationFirewallPolicy#managed_rules}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#name WebApplicationFirewallPolicy#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#resource_group_name WebApplicationFirewallPolicy#resource_group_name}.
        :param custom_rules: custom_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#custom_rules WebApplicationFirewallPolicy#custom_rules}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#id WebApplicationFirewallPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_settings: policy_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#policy_settings WebApplicationFirewallPolicy#policy_settings}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#tags WebApplicationFirewallPolicy#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#timeouts WebApplicationFirewallPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(managed_rules, dict):
            managed_rules = WebApplicationFirewallPolicyManagedRules(**managed_rules)
        if isinstance(policy_settings, dict):
            policy_settings = WebApplicationFirewallPolicyPolicySettings(**policy_settings)
        if isinstance(timeouts, dict):
            timeouts = WebApplicationFirewallPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d2f6ee18d83e4c9c3d3ef24a41c0c488488492179ef22b6e741b2367ca3677)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument managed_rules", value=managed_rules, expected_type=type_hints["managed_rules"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument custom_rules", value=custom_rules, expected_type=type_hints["custom_rules"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy_settings", value=policy_settings, expected_type=type_hints["policy_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "managed_rules": managed_rules,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if custom_rules is not None:
            self._values["custom_rules"] = custom_rules
        if id is not None:
            self._values["id"] = id
        if policy_settings is not None:
            self._values["policy_settings"] = policy_settings
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#location WebApplicationFirewallPolicy#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def managed_rules(self) -> "WebApplicationFirewallPolicyManagedRules":
        '''managed_rules block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#managed_rules WebApplicationFirewallPolicy#managed_rules}
        '''
        result = self._values.get("managed_rules")
        assert result is not None, "Required property 'managed_rules' is missing"
        return typing.cast("WebApplicationFirewallPolicyManagedRules", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#name WebApplicationFirewallPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#resource_group_name WebApplicationFirewallPolicy#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyCustomRules"]]]:
        '''custom_rules block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#custom_rules WebApplicationFirewallPolicy#custom_rules}
        '''
        result = self._values.get("custom_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyCustomRules"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#id WebApplicationFirewallPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_settings(
        self,
    ) -> typing.Optional["WebApplicationFirewallPolicyPolicySettings"]:
        '''policy_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#policy_settings WebApplicationFirewallPolicy#policy_settings}
        '''
        result = self._values.get("policy_settings")
        return typing.cast(typing.Optional["WebApplicationFirewallPolicyPolicySettings"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#tags WebApplicationFirewallPolicy#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WebApplicationFirewallPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#timeouts WebApplicationFirewallPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WebApplicationFirewallPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRules",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match_conditions": "matchConditions",
        "priority": "priority",
        "rule_type": "ruleType",
        "name": "name",
    },
)
class WebApplicationFirewallPolicyCustomRules:
    def __init__(
        self,
        *,
        action: builtins.str,
        match_conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyCustomRulesMatchConditions", typing.Dict[builtins.str, typing.Any]]]],
        priority: jsii.Number,
        rule_type: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#action WebApplicationFirewallPolicy#action}.
        :param match_conditions: match_conditions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#match_conditions WebApplicationFirewallPolicy#match_conditions}
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#priority WebApplicationFirewallPolicy#priority}.
        :param rule_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_type WebApplicationFirewallPolicy#rule_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#name WebApplicationFirewallPolicy#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4246944b4b2e7e34ba8c1db94daf3e1f12bb5b6b9b3928d7eb70fc8d6f3a6299)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match_conditions", value=match_conditions, expected_type=type_hints["match_conditions"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument rule_type", value=rule_type, expected_type=type_hints["rule_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match_conditions": match_conditions,
            "priority": priority,
            "rule_type": rule_type,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#action WebApplicationFirewallPolicy#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyCustomRulesMatchConditions"]]:
        '''match_conditions block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#match_conditions WebApplicationFirewallPolicy#match_conditions}
        '''
        result = self._values.get("match_conditions")
        assert result is not None, "Required property 'match_conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyCustomRulesMatchConditions"]], result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#priority WebApplicationFirewallPolicy#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rule_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_type WebApplicationFirewallPolicy#rule_type}.'''
        result = self._values.get("rule_type")
        assert result is not None, "Required property 'rule_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#name WebApplicationFirewallPolicy#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyCustomRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyCustomRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRulesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e3ed0eff23126aed564a729c2b6ed7746dca803b8f8aaef9aa9fb140590bb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebApplicationFirewallPolicyCustomRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1511b04aafcf867e6fc40bd43041623b43a5f6849a3492a902af843f5e035a93)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebApplicationFirewallPolicyCustomRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575daf3ccb6cd61fc145f633e5d7103e5b47a0ad6605c741f2645264c53ade4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df795bcb367317dbe6fee0e41fc142c931f397ac6420f0f4eabf72954beba0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb7bea28c8f3be597c35991aeefb969726bfa1f08dce062bcb7dfd05f55406e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7df2a0eb61c1b2ac372c144a80e651d08422555bbd264d417afdad46827307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRulesMatchConditions",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "match_variables": "matchVariables",
        "operator": "operator",
        "negation_condition": "negationCondition",
        "transforms": "transforms",
    },
)
class WebApplicationFirewallPolicyCustomRulesMatchConditions:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        match_variables: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables", typing.Dict[builtins.str, typing.Any]]]],
        operator: builtins.str,
        negation_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#match_values WebApplicationFirewallPolicy#match_values}.
        :param match_variables: match_variables block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#match_variables WebApplicationFirewallPolicy#match_variables}
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#operator WebApplicationFirewallPolicy#operator}.
        :param negation_condition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#negation_condition WebApplicationFirewallPolicy#negation_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#transforms WebApplicationFirewallPolicy#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c73f3450f2944ed30117501bea6207a91346252cb773eff29182b6fe2da016)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument match_variables", value=match_variables, expected_type=type_hints["match_variables"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument negation_condition", value=negation_condition, expected_type=type_hints["negation_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_values": match_values,
            "match_variables": match_variables,
            "operator": operator,
        }
        if negation_condition is not None:
            self._values["negation_condition"] = negation_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def match_values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#match_values WebApplicationFirewallPolicy#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def match_variables(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables"]]:
        '''match_variables block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#match_variables WebApplicationFirewallPolicy#match_variables}
        '''
        result = self._values.get("match_variables")
        assert result is not None, "Required property 'match_variables' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables"]], result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#operator WebApplicationFirewallPolicy#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def negation_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#negation_condition WebApplicationFirewallPolicy#negation_condition}.'''
        result = self._values.get("negation_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#transforms WebApplicationFirewallPolicy#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyCustomRulesMatchConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyCustomRulesMatchConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRulesMatchConditionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98a5bc87db62d1f78dc405c31515707b2c4ca6345cf36f5731d8acbe989cf11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebApplicationFirewallPolicyCustomRulesMatchConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92f43bda64b5e86826e3515b7165f4cf947071c45106c34e78abec737965c7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebApplicationFirewallPolicyCustomRulesMatchConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32a5ea8546b6473d174c26aa0100d14292bdd53c6d85a4e21269c9ecb3f4d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e3d55ca649bb17db12cb4e9e0e601a655c836e6a82bb1e2448aab23232efb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51dda831f505c5a5033fe3e0d1eac40c11d2dd490db273b3c602d65c9453d524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645a55f88a73973d3d5850ecbfa10795cfdc54ad2d25b5fbf7b40d9060f34b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables",
    jsii_struct_bases=[],
    name_mapping={"variable_name": "variableName", "selector": "selector"},
)
class WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables:
    def __init__(
        self,
        *,
        variable_name: builtins.str,
        selector: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param variable_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#variable_name WebApplicationFirewallPolicy#variable_name}.
        :param selector: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#selector WebApplicationFirewallPolicy#selector}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea398cedb4277c999282f5d0f6e60de6fb225a5433489bfce8435897e910aa89)
            check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "variable_name": variable_name,
        }
        if selector is not None:
            self._values["selector"] = selector

    @builtins.property
    def variable_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#variable_name WebApplicationFirewallPolicy#variable_name}.'''
        result = self._values.get("variable_name")
        assert result is not None, "Required property 'variable_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#selector WebApplicationFirewallPolicy#selector}.'''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083a6f1459417b6936e2cfbdd205f17a80cbcdf06745d6098569ed8bd0ff727c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4127f00bb170181240150807691fb9ec82ca60feae02614631b1eceb5a26d031)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74d08b30411e886baec5499ba42d48224e7179cacb98164a20572df633b9aea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff6c88b3210de25a9a43db2b5c8709661801540c7c7f5c2e59acb2eca5e093f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9553de99396232f4fda896e79f69ba030a33b9c699be70d4c3f5637d91a66f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88d900166f1d8df89878f57489c3df6fcb8ad311bab75665e15e7a7ea5acb6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909dd441e5f0f1851ea51ec5e44964382b1c6006640d563ae33f14a55c2b6384)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="variableNameInput")
    def variable_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b655bbcafcecca6445dcf9197b04e05d56ae54d0cb4fa835c0c6ef1e0a77eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value)

    @builtins.property
    @jsii.member(jsii_name="variableName")
    def variable_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variableName"))

    @variable_name.setter
    def variable_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad957fb3fbd8b9219805d68c056d40d0f7d420a4a53d28ea076585cb38e368a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variableName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e295e257e3d3fbab7bfd25f12e8300a45bccc3b286a1f77e7482c46fe02e18a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyCustomRulesMatchConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRulesMatchConditionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc4f2df3320a78fcf2ce57e657f1be12c7a036412af36e2db4202e94f2b8cbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchVariables")
    def put_match_variables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d73b92adc1b3810f5db90ad27cd17162c2e82b4781da8027aa809c41e19ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchVariables", [value]))

    @jsii.member(jsii_name="resetNegationCondition")
    def reset_negation_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegationCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchVariables")
    def match_variables(
        self,
    ) -> WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesList:
        return typing.cast(WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesList, jsii.get(self, "matchVariables"))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchVariablesInput")
    def match_variables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables]]], jsii.get(self, "matchVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="negationConditionInput")
    def negation_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negationConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fcd9488f3a6de325ffe729b482f524fe23c215b06c7602693beb435b79d574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value)

    @builtins.property
    @jsii.member(jsii_name="negationCondition")
    def negation_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negationCondition"))

    @negation_condition.setter
    def negation_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ca3ac34b643131a5cb5b381c85592ca438194e4a25328039e1990886eafbd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negationCondition", value)

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618b4bc6936bd066382f684d4e8d2865454a933b4c9d7c3665a0b38a03c57f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c14aa69a740d68282ae7204b862ef0fc7802e7140d1d9cada713311d201d2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditions, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditions, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditions, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a3dfdcd5a9287f9ae9b58fdd8256fba4fb0b71c863619429458f4a73b8b394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyCustomRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyCustomRulesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c5b7655ecadee89bc5f6d6e243155ed4ccc140bf178557756f0ab6248f617c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchConditions")
    def put_match_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a58165d5b271f41dad391a6f786bc99c7bee87631a512734a7fe138cd9f41d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchConditions", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="matchConditions")
    def match_conditions(
        self,
    ) -> WebApplicationFirewallPolicyCustomRulesMatchConditionsList:
        return typing.cast(WebApplicationFirewallPolicyCustomRulesMatchConditionsList, jsii.get(self, "matchConditions"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchConditionsInput")
    def match_conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditions]]], jsii.get(self, "matchConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleTypeInput")
    def rule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c551a5fe90596ea8dd228222d082becd5c1dda74abfa363f75a4d8c546c82f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be51241b32b2b8042298611fa8ece10ef189c6a184cd1a5ad14988a68076988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd04fb2683240fc39d1e9d804b8c1aeb8a40f34f7041c25ab56ba2d7b2de933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1101b0cb63373d766d8706c7f1c2691a47a061b65e0c91d4cdf561cc14162cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRules, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRules, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRules, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e0c8cd541cc91a8d1d3d185ebe0533bda843d6c2d5356b2fdff555e42dbbde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRules",
    jsii_struct_bases=[],
    name_mapping={"managed_rule_set": "managedRuleSet", "exclusion": "exclusion"},
)
class WebApplicationFirewallPolicyManagedRules:
    def __init__(
        self,
        *,
        managed_rule_set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesManagedRuleSet", typing.Dict[builtins.str, typing.Any]]]],
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param managed_rule_set: managed_rule_set block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#managed_rule_set WebApplicationFirewallPolicy#managed_rule_set}
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#exclusion WebApplicationFirewallPolicy#exclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40cc4fc62803753273cb33e670c1da68e19ef01b67231cd938083eed6e02ff97)
            check_type(argname="argument managed_rule_set", value=managed_rule_set, expected_type=type_hints["managed_rule_set"])
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "managed_rule_set": managed_rule_set,
        }
        if exclusion is not None:
            self._values["exclusion"] = exclusion

    @builtins.property
    def managed_rule_set(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSet"]]:
        '''managed_rule_set block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#managed_rule_set WebApplicationFirewallPolicy#managed_rule_set}
        '''
        result = self._values.get("managed_rule_set")
        assert result is not None, "Required property 'managed_rule_set' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSet"]], result)

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesExclusion"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#exclusion WebApplicationFirewallPolicy#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesExclusion"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyManagedRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesExclusion",
    jsii_struct_bases=[],
    name_mapping={
        "match_variable": "matchVariable",
        "selector": "selector",
        "selector_match_operator": "selectorMatchOperator",
        "excluded_rule_set": "excludedRuleSet",
    },
)
class WebApplicationFirewallPolicyManagedRulesExclusion:
    def __init__(
        self,
        *,
        match_variable: builtins.str,
        selector: builtins.str,
        selector_match_operator: builtins.str,
        excluded_rule_set: typing.Optional[typing.Union["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param match_variable: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#match_variable WebApplicationFirewallPolicy#match_variable}.
        :param selector: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#selector WebApplicationFirewallPolicy#selector}.
        :param selector_match_operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#selector_match_operator WebApplicationFirewallPolicy#selector_match_operator}.
        :param excluded_rule_set: excluded_rule_set block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#excluded_rule_set WebApplicationFirewallPolicy#excluded_rule_set}
        '''
        if isinstance(excluded_rule_set, dict):
            excluded_rule_set = WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet(**excluded_rule_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70b68215100175efa2b87cb94f3e890c3c32499a77820d2e8677c48727b432c)
            check_type(argname="argument match_variable", value=match_variable, expected_type=type_hints["match_variable"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument selector_match_operator", value=selector_match_operator, expected_type=type_hints["selector_match_operator"])
            check_type(argname="argument excluded_rule_set", value=excluded_rule_set, expected_type=type_hints["excluded_rule_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_variable": match_variable,
            "selector": selector,
            "selector_match_operator": selector_match_operator,
        }
        if excluded_rule_set is not None:
            self._values["excluded_rule_set"] = excluded_rule_set

    @builtins.property
    def match_variable(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#match_variable WebApplicationFirewallPolicy#match_variable}.'''
        result = self._values.get("match_variable")
        assert result is not None, "Required property 'match_variable' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#selector WebApplicationFirewallPolicy#selector}.'''
        result = self._values.get("selector")
        assert result is not None, "Required property 'selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector_match_operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#selector_match_operator WebApplicationFirewallPolicy#selector_match_operator}.'''
        result = self._values.get("selector_match_operator")
        assert result is not None, "Required property 'selector_match_operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def excluded_rule_set(
        self,
    ) -> typing.Optional["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet"]:
        '''excluded_rule_set block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#excluded_rule_set WebApplicationFirewallPolicy#excluded_rule_set}
        '''
        result = self._values.get("excluded_rule_set")
        return typing.cast(typing.Optional["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyManagedRulesExclusion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet",
    jsii_struct_bases=[],
    name_mapping={"rule_group": "ruleGroup", "type": "type", "version": "version"},
)
class WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet:
    def __init__(
        self,
        *,
        rule_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rule_group: rule_group block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group WebApplicationFirewallPolicy#rule_group}
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#type WebApplicationFirewallPolicy#type}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#version WebApplicationFirewallPolicy#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2030e0236826474a31e23891bf94b91f01c4b3b0f4b0f34e1e6d640f77e3ffe0)
            check_type(argname="argument rule_group", value=rule_group, expected_type=type_hints["rule_group"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule_group is not None:
            self._values["rule_group"] = rule_group
        if type is not None:
            self._values["type"] = type
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def rule_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup"]]]:
        '''rule_group block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group WebApplicationFirewallPolicy#rule_group}
        '''
        result = self._values.get("rule_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#type WebApplicationFirewallPolicy#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#version WebApplicationFirewallPolicy#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0e94fa767b6f3dcb19653301f0517c1c1027e69800672fab5ab7c8f91fe3e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRuleGroup")
    def put_rule_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9806d009c17afbf48b74a4d8e4fcd81f98b6e13a5eff7431f319b0dfb0660dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRuleGroup", [value]))

    @jsii.member(jsii_name="resetRuleGroup")
    def reset_rule_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleGroup", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="ruleGroup")
    def rule_group(
        self,
    ) -> "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupList":
        return typing.cast("WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupList", jsii.get(self, "ruleGroup"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupInput")
    def rule_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup"]]], jsii.get(self, "ruleGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170160d764e50e45a65627e931f64d266f10aa9fc402a533d205c462a3ce543e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b49f31f60be8a2fc5d65d21fa4a222cdbb52e5574e55deb1b5e64b0a373ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet]:
        return typing.cast(typing.Optional[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0a12c815bb9e469617fb84b7fb41900149943968a5ac5bf94216e19b24098e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup",
    jsii_struct_bases=[],
    name_mapping={
        "rule_group_name": "ruleGroupName",
        "excluded_rules": "excludedRules",
    },
)
class WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup:
    def __init__(
        self,
        *,
        rule_group_name: builtins.str,
        excluded_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param rule_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group_name WebApplicationFirewallPolicy#rule_group_name}.
        :param excluded_rules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#excluded_rules WebApplicationFirewallPolicy#excluded_rules}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503b82481225d3a0f8461f4dce7620bba0c07127c8cfe170d5ae80b13eb476e9)
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument excluded_rules", value=excluded_rules, expected_type=type_hints["excluded_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_group_name": rule_group_name,
        }
        if excluded_rules is not None:
            self._values["excluded_rules"] = excluded_rules

    @builtins.property
    def rule_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group_name WebApplicationFirewallPolicy#rule_group_name}.'''
        result = self._values.get("rule_group_name")
        assert result is not None, "Required property 'rule_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def excluded_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#excluded_rules WebApplicationFirewallPolicy#excluded_rules}.'''
        result = self._values.get("excluded_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a276a39e3e8ea536a0d2220d89cf22ac16ad46ad65e599c31e920b41a7ce53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f345de297cd33325a07e002ffc833657edc2a859a9cadb0b9d25e76beef249)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b28722ce8c46a0e7d61f168763d5f922d59684c5a2632c677430d34cbe85381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f87b31aff2faed6c836e35e5edb38a4bce9e264db911b3ac93b4951465e282b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e560cf2bb2a8ffb1cfe016f20da2352cd8567508edd0e24d23bdf0e8e0ebb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c74c6fed9e4da6d22d8ea0cab0146a98e86db6d66adc4a9538feecb0608b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345daa111f3fe85c603d16f1a2385433f9578b1f598af97bc5d59369764c08a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExcludedRules")
    def reset_excluded_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedRules", []))

    @builtins.property
    @jsii.member(jsii_name="excludedRulesInput")
    def excluded_rules_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupNameInput")
    def rule_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedRules")
    def excluded_rules(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedRules"))

    @excluded_rules.setter
    def excluded_rules(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f8929e27c67fce7a4157d1ac57c9d8c71f79ef2ecf67239e67f0db453802d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedRules", value)

    @builtins.property
    @jsii.member(jsii_name="ruleGroupName")
    def rule_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupName"))

    @rule_group_name.setter
    def rule_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82afea227f83e75472151f0212fe0582bb1bf713dccaf00dd8d28d8b3219605a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cf264c5d837177e3a817643c4efe522bfb33b91339fb8b0f5793b31f528fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyManagedRulesExclusionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesExclusionList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f90932898c1cb4e70c8ef47a077bfe7614133dd06a4b39982abe3a143ea7fcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebApplicationFirewallPolicyManagedRulesExclusionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d74fed3fc4ea55ac93d87521f5947cba5250e6d9acb4f3ced679608b508d047)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebApplicationFirewallPolicyManagedRulesExclusionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41caf9b08556fc13f5c0d84dbd523a6c2518d2c8df9279e8328a162f4ff9285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1243d77b9efd748bd62d8a19a0e4a657ad0019a5ae3183fe9ed4b88f25edee88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8111e0b10ce713348b0c1b08a4296d612754519708395889bc6c85a0f10f203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35dbd1f831e96a422f8eac06d8f80e2fbc0d4c420f4a92ccf170c001bcf2376d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyManagedRulesExclusionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesExclusionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e175f75598d9eb32b13553acd7d18f26432f90931313e899c5b71fd69a613488)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExcludedRuleSet")
    def put_excluded_rule_set(
        self,
        *,
        rule_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rule_group: rule_group block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group WebApplicationFirewallPolicy#rule_group}
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#type WebApplicationFirewallPolicy#type}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#version WebApplicationFirewallPolicy#version}.
        '''
        value = WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet(
            rule_group=rule_group, type=type, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putExcludedRuleSet", [value]))

    @jsii.member(jsii_name="resetExcludedRuleSet")
    def reset_excluded_rule_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedRuleSet", []))

    @builtins.property
    @jsii.member(jsii_name="excludedRuleSet")
    def excluded_rule_set(
        self,
    ) -> WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetOutputReference:
        return typing.cast(WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetOutputReference, jsii.get(self, "excludedRuleSet"))

    @builtins.property
    @jsii.member(jsii_name="excludedRuleSetInput")
    def excluded_rule_set_input(
        self,
    ) -> typing.Optional[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet]:
        return typing.cast(typing.Optional[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet], jsii.get(self, "excludedRuleSetInput"))

    @builtins.property
    @jsii.member(jsii_name="matchVariableInput")
    def match_variable_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorMatchOperatorInput")
    def selector_match_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorMatchOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="matchVariable")
    def match_variable(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchVariable"))

    @match_variable.setter
    def match_variable(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d330385f4186fa21ff9db8b08e9748719cc2676b2510b33a452fa872e2af46c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchVariable", value)

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0c20113c250ca5000ff6f12f78f0fede19ec2094850983ed18fa3bc3bd2326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value)

    @builtins.property
    @jsii.member(jsii_name="selectorMatchOperator")
    def selector_match_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selectorMatchOperator"))

    @selector_match_operator.setter
    def selector_match_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fd3441066736d7b03d5f4c0cdca345539f245691cf2d1b031631b4ebc9eae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectorMatchOperator", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusion, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusion, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusion, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57313187c06a7cacf494cda3d489205116b617949983e7e823a5f3957e467342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSet",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "rule_group_override": "ruleGroupOverride",
        "type": "type",
    },
)
class WebApplicationFirewallPolicyManagedRulesManagedRuleSet:
    def __init__(
        self,
        *,
        version: builtins.str,
        rule_group_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#version WebApplicationFirewallPolicy#version}.
        :param rule_group_override: rule_group_override block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group_override WebApplicationFirewallPolicy#rule_group_override}
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#type WebApplicationFirewallPolicy#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2ed48eff12b7310a3ecb0d28aa8683486ada8d18ece389378657482bee885f)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument rule_group_override", value=rule_group_override, expected_type=type_hints["rule_group_override"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if rule_group_override is not None:
            self._values["rule_group_override"] = rule_group_override
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#version WebApplicationFirewallPolicy#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_group_override(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride"]]]:
        '''rule_group_override block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group_override WebApplicationFirewallPolicy#rule_group_override}
        '''
        result = self._values.get("rule_group_override")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#type WebApplicationFirewallPolicy#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyManagedRulesManagedRuleSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyManagedRulesManagedRuleSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSetList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132fec163686efa8ad697d7a2599c78cb1891e4064f310dec662ea6b8c0f41f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebApplicationFirewallPolicyManagedRulesManagedRuleSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669e96bf7bc9992bbb965d33f5bb9b7a288533a69d2f499231b913dad7a4842c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebApplicationFirewallPolicyManagedRulesManagedRuleSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0626a796a6816e4811883866dfe4b827034b6d4d155bbb6c02f91f1bdcb8c579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe571c82b61ce5b8abbebe58a1b7b81c56c916ee09fee40c4a4f55589917f6e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f00ceb1d577e9fd2923f495871d2c438663104e13c18942dab7ef2fcb6ab99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aabcfd894067ca4448948edbedacd9bd43a5d6f1f16b7926375a96366612d67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyManagedRulesManagedRuleSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSetOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa1dc0524d20a97a43ff69ec7ddf9b09ab6b67816ffb3856ed6f6b5549dad94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRuleGroupOverride")
    def put_rule_group_override(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3b97108df2df9fe04729ff829398728a93c85730c90951ce69846a885e51b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRuleGroupOverride", [value]))

    @jsii.member(jsii_name="resetRuleGroupOverride")
    def reset_rule_group_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleGroupOverride", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupOverride")
    def rule_group_override(
        self,
    ) -> "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideList":
        return typing.cast("WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideList", jsii.get(self, "ruleGroupOverride"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupOverrideInput")
    def rule_group_override_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride"]]], jsii.get(self, "ruleGroupOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0478cb6000d7d8a769e7b4767e8cf7165cdabeed13aff2aa2a3fe9b0668f57cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddbe07479482f3c638e19440e0e764903e286c18a78466e5ae050f48ec619733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSet, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSet, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSet, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a361572360604fafef8e9958bb99b9ba1f7117760e0a9bb1ab7344a45a1757a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride",
    jsii_struct_bases=[],
    name_mapping={
        "rule_group_name": "ruleGroupName",
        "disabled_rules": "disabledRules",
        "rule": "rule",
    },
)
class WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride:
    def __init__(
        self,
        *,
        rule_group_name: builtins.str,
        disabled_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group_name WebApplicationFirewallPolicy#rule_group_name}.
        :param disabled_rules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#disabled_rules WebApplicationFirewallPolicy#disabled_rules}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule WebApplicationFirewallPolicy#rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565bbc45342f5657b1e2bb716ca15d5e8f29266bd03e70c94393ff6ce55b669c)
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument disabled_rules", value=disabled_rules, expected_type=type_hints["disabled_rules"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_group_name": rule_group_name,
        }
        if disabled_rules is not None:
            self._values["disabled_rules"] = disabled_rules
        if rule is not None:
            self._values["rule"] = rule

    @builtins.property
    def rule_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule_group_name WebApplicationFirewallPolicy#rule_group_name}.'''
        result = self._values.get("rule_group_name")
        assert result is not None, "Required property 'rule_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disabled_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#disabled_rules WebApplicationFirewallPolicy#disabled_rules}.'''
        result = self._values.get("disabled_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#rule WebApplicationFirewallPolicy#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91428f019523e09551f5fcdbb30ad3e27732367a583290c68c8ed5dcc0bafbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21920fb438c0a6da8f1dcad92f897c7f98842fcccb9f6bd5e1ede6ae57337c1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee72a83a612016fc7e0f1edbd2b5b111e0a74a4da12027a1b9bcb0cb3332afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348d0969fd3e1fc652f89c3d08293248c57722ba054cf3a5c6d467c54ac05a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332acbd063f34d0907caec64bd310fe26b1aeb430bface1abe2259fe97c5469d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45cb841b1b4798a8671bc6a16819af3a3de78a3fdd666ec8de87f5ddd167b1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d085613a12c524a1655a9021103fa76f00b65ef1ac28e89222acc0473704f011)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2186422b28e78bbff9f3448c0cf6395262d0103df7ccc38c1cf6599a50c4cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetDisabledRules")
    def reset_disabled_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledRules", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(
        self,
    ) -> "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleList":
        return typing.cast("WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="disabledRulesInput")
    def disabled_rules_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "disabledRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupNameInput")
    def rule_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledRules")
    def disabled_rules(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "disabledRules"))

    @disabled_rules.setter
    def disabled_rules(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11cbbf77410a7ea0ff5202d9f12b487025b4f56729e938c0fd8352e30512fd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledRules", value)

    @builtins.property
    @jsii.member(jsii_name="ruleGroupName")
    def rule_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupName"))

    @rule_group_name.setter
    def rule_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f92f1d99bd8dc4524b622ae1fa71e0c15ab0a766ee3327585761d3bac23d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4fdbafdd83120b6e9064e910e67691c73ffd7bff5c816f5302eb94d5a9505b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "action": "action", "enabled": "enabled"},
)
class WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        action: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#id WebApplicationFirewallPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#action WebApplicationFirewallPolicy#action}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#enabled WebApplicationFirewallPolicy#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3315631081e2aff3aa78e80ca91322ca8bd3c736265815c1d717aa17d29ea060)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if action is not None:
            self._values["action"] = action
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#id WebApplicationFirewallPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#action WebApplicationFirewallPolicy#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#enabled WebApplicationFirewallPolicy#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728b4c0434fbae523e360133549cd13c2d08098b8bfcbb5e793b886f60a000a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92abfadd4ddfaf4f582423d4a7fc64121b8daff470165cb7ec627f3eb1324454)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c6cb78ab3f95583867147d6bcbdf7a544f1ad73f92739a019fcee41f06dce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414bd8377e47d8712ebe6e0c9fe5e6b45fe324d764ba2b90c2c7413a231d78a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df808ee9f1e48b623630ff4ba043f7475adc51c0be3dab5e9fc5248cbd7895e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d240b278e0599697c25ab741a3abe10eb485a467c5be1cbfba9dcd7ef376ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde31467de9dbe9db106247d733fb7bffd27a2073346b02642efa2a0200d0429)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4a2752917672057890d7fe6bd472971e0deba6c3d3b7f97692d32a9714592e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__aa11ec1a0b1aad6fb9f2a084545f13011a3a28357781d37dfe1e85143a6656ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f679d790754665005be1c05149ec887557698801fbdb5900a0162aacb4cc1666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e406ef60bf78a21c01eda4b9ace8edfa538ea90a0aa9b5d0e2a927059430372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WebApplicationFirewallPolicyManagedRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyManagedRulesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dabc846cc38cf79e54f128199399775fb63695094eae04920af1cd099d44d763)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0a611ab3def21f8c094a0444669431914e9659b3537b1cd6504d668c3b33bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="putManagedRuleSet")
    def put_managed_rule_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSet, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28a1d166dc4b2033064670fc263591939ac519d96198795448d5410a1641633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedRuleSet", [value]))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(self) -> WebApplicationFirewallPolicyManagedRulesExclusionList:
        return typing.cast(WebApplicationFirewallPolicyManagedRulesExclusionList, jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="managedRuleSet")
    def managed_rule_set(
        self,
    ) -> WebApplicationFirewallPolicyManagedRulesManagedRuleSetList:
        return typing.cast(WebApplicationFirewallPolicyManagedRulesManagedRuleSetList, jsii.get(self, "managedRuleSet"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusion]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="managedRuleSetInput")
    def managed_rule_set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSet]]], jsii.get(self, "managedRuleSetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WebApplicationFirewallPolicyManagedRules]:
        return typing.cast(typing.Optional[WebApplicationFirewallPolicyManagedRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WebApplicationFirewallPolicyManagedRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493d605c900437f2bcab548a9e697f7e945537b25ae66285b275ddea96ddcb3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyPolicySettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "file_upload_limit_in_mb": "fileUploadLimitInMb",
        "max_request_body_size_in_kb": "maxRequestBodySizeInKb",
        "mode": "mode",
        "request_body_check": "requestBodyCheck",
    },
)
class WebApplicationFirewallPolicyPolicySettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_upload_limit_in_mb: typing.Optional[jsii.Number] = None,
        max_request_body_size_in_kb: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
        request_body_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#enabled WebApplicationFirewallPolicy#enabled}.
        :param file_upload_limit_in_mb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#file_upload_limit_in_mb WebApplicationFirewallPolicy#file_upload_limit_in_mb}.
        :param max_request_body_size_in_kb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#max_request_body_size_in_kb WebApplicationFirewallPolicy#max_request_body_size_in_kb}.
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#mode WebApplicationFirewallPolicy#mode}.
        :param request_body_check: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#request_body_check WebApplicationFirewallPolicy#request_body_check}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d8810ab0fdf088714565f941f3d9d04e09286411c4c83d6f04807101e90b91)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument file_upload_limit_in_mb", value=file_upload_limit_in_mb, expected_type=type_hints["file_upload_limit_in_mb"])
            check_type(argname="argument max_request_body_size_in_kb", value=max_request_body_size_in_kb, expected_type=type_hints["max_request_body_size_in_kb"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument request_body_check", value=request_body_check, expected_type=type_hints["request_body_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if file_upload_limit_in_mb is not None:
            self._values["file_upload_limit_in_mb"] = file_upload_limit_in_mb
        if max_request_body_size_in_kb is not None:
            self._values["max_request_body_size_in_kb"] = max_request_body_size_in_kb
        if mode is not None:
            self._values["mode"] = mode
        if request_body_check is not None:
            self._values["request_body_check"] = request_body_check

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#enabled WebApplicationFirewallPolicy#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def file_upload_limit_in_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#file_upload_limit_in_mb WebApplicationFirewallPolicy#file_upload_limit_in_mb}.'''
        result = self._values.get("file_upload_limit_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_request_body_size_in_kb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#max_request_body_size_in_kb WebApplicationFirewallPolicy#max_request_body_size_in_kb}.'''
        result = self._values.get("max_request_body_size_in_kb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#mode WebApplicationFirewallPolicy#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_body_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#request_body_check WebApplicationFirewallPolicy#request_body_check}.'''
        result = self._values.get("request_body_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyPolicySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyPolicySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyPolicySettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942c3184a64a4fe9eef9a703f6eb3d14cb979dae8ec1fa7ef4ca37e63205007b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFileUploadLimitInMb")
    def reset_file_upload_limit_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUploadLimitInMb", []))

    @jsii.member(jsii_name="resetMaxRequestBodySizeInKb")
    def reset_max_request_body_size_in_kb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRequestBodySizeInKb", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetRequestBodyCheck")
    def reset_request_body_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBodyCheck", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUploadLimitInMbInput")
    def file_upload_limit_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileUploadLimitInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRequestBodySizeInKbInput")
    def max_request_body_size_in_kb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRequestBodySizeInKbInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyCheckInput")
    def request_body_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestBodyCheckInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ace765a3a2296695c26a4c4d3bfb92bc2e8837e010447648596e4f0af8973c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="fileUploadLimitInMb")
    def file_upload_limit_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileUploadLimitInMb"))

    @file_upload_limit_in_mb.setter
    def file_upload_limit_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8089efcc73a4a5c5fda5ab3651e04969cc6afb53d55de0299feefa02101847b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUploadLimitInMb", value)

    @builtins.property
    @jsii.member(jsii_name="maxRequestBodySizeInKb")
    def max_request_body_size_in_kb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequestBodySizeInKb"))

    @max_request_body_size_in_kb.setter
    def max_request_body_size_in_kb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebc4ea9759c6e6edb779bb42089e6bd3eb5e8dcaafaa0d1919d86af98e1827c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequestBodySizeInKb", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d0ead72df80e9e994943aa9401105538ce0ada059ef445cd07e211e1a743ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="requestBodyCheck")
    def request_body_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestBodyCheck"))

    @request_body_check.setter
    def request_body_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec953f5e203ada9a9618e25b4195ea6ddbdfc2a27860dd8198cd3365ad87adb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestBodyCheck", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WebApplicationFirewallPolicyPolicySettings]:
        return typing.cast(typing.Optional[WebApplicationFirewallPolicyPolicySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WebApplicationFirewallPolicyPolicySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b352f36194865fa8304561959b4dfda2b5a4a095556d250bc6c112b876b9f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class WebApplicationFirewallPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#create WebApplicationFirewallPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#delete WebApplicationFirewallPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#read WebApplicationFirewallPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#update WebApplicationFirewallPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177e788400e574657bb756209d0d909c96d1296975a0e5d7fd5f0646178c9254)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#create WebApplicationFirewallPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#delete WebApplicationFirewallPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#read WebApplicationFirewallPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/web_application_firewall_policy#update WebApplicationFirewallPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebApplicationFirewallPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebApplicationFirewallPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webApplicationFirewallPolicy.WebApplicationFirewallPolicyTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb695d025c665f6855f0dd2edb30e9c1c48126dfe9f4057907432dd8efc349b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca17d34c2deb57dc278db6976afbd486956e2271691efeb5c4f5010e86edc239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a56e002359db65375a6457500c60f95f593deba260c7e010d02258b3d12b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7070dcbb8cd1fc65651b4e80e6c430816d8b8bfbc78e66130280672ac8ff7330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5be38e1628ae9f34795149502cfa557d595cb4a3a429a4bf5a695c67581c91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WebApplicationFirewallPolicyTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WebApplicationFirewallPolicyTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WebApplicationFirewallPolicyTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4044755143e3c3251666ec3da3d2fdf3e4e96b4d32fc1785d4af9387fca7383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "WebApplicationFirewallPolicy",
    "WebApplicationFirewallPolicyConfig",
    "WebApplicationFirewallPolicyCustomRules",
    "WebApplicationFirewallPolicyCustomRulesList",
    "WebApplicationFirewallPolicyCustomRulesMatchConditions",
    "WebApplicationFirewallPolicyCustomRulesMatchConditionsList",
    "WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables",
    "WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesList",
    "WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariablesOutputReference",
    "WebApplicationFirewallPolicyCustomRulesMatchConditionsOutputReference",
    "WebApplicationFirewallPolicyCustomRulesOutputReference",
    "WebApplicationFirewallPolicyManagedRules",
    "WebApplicationFirewallPolicyManagedRulesExclusion",
    "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet",
    "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetOutputReference",
    "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup",
    "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupList",
    "WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroupOutputReference",
    "WebApplicationFirewallPolicyManagedRulesExclusionList",
    "WebApplicationFirewallPolicyManagedRulesExclusionOutputReference",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSet",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSetList",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSetOutputReference",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideList",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideOutputReference",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleList",
    "WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRuleOutputReference",
    "WebApplicationFirewallPolicyManagedRulesOutputReference",
    "WebApplicationFirewallPolicyPolicySettings",
    "WebApplicationFirewallPolicyPolicySettingsOutputReference",
    "WebApplicationFirewallPolicyTimeouts",
    "WebApplicationFirewallPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1d1011c6efdc5e09194917c9842844a514e10ed7f3cc1bf5d64300d10b4ccd31(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    managed_rules: typing.Union[WebApplicationFirewallPolicyManagedRules, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    resource_group_name: builtins.str,
    custom_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    policy_settings: typing.Optional[typing.Union[WebApplicationFirewallPolicyPolicySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[WebApplicationFirewallPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__00b3ba5b93c7d443377ec1979a61bb716a3631f7f4043448316103ce0398010f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e287fc0aa7f9aca943799bee97133b366f1fca39d1acfa3dc28e462e94aefa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ffe5a05a5fea90affba48e7d91a5ad66a399ff58003324401ba2a84f597652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e275007680d9ba18e2b5c015ecf8d383e4bdd288ef280cc1c5240c316d3389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf3bc8e89a2fe42ee30cb3da287cce95217b95ba05f0b24650026931edb52e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e2229c572be7b31330f4059f72c8b582f4d8c7b197a176a357676514473a64(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d2f6ee18d83e4c9c3d3ef24a41c0c488488492179ef22b6e741b2367ca3677(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    managed_rules: typing.Union[WebApplicationFirewallPolicyManagedRules, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    resource_group_name: builtins.str,
    custom_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    policy_settings: typing.Optional[typing.Union[WebApplicationFirewallPolicyPolicySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[WebApplicationFirewallPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4246944b4b2e7e34ba8c1db94daf3e1f12bb5b6b9b3928d7eb70fc8d6f3a6299(
    *,
    action: builtins.str,
    match_conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditions, typing.Dict[builtins.str, typing.Any]]]],
    priority: jsii.Number,
    rule_type: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e3ed0eff23126aed564a729c2b6ed7746dca803b8f8aaef9aa9fb140590bb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1511b04aafcf867e6fc40bd43041623b43a5f6849a3492a902af843f5e035a93(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575daf3ccb6cd61fc145f633e5d7103e5b47a0ad6605c741f2645264c53ade4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df795bcb367317dbe6fee0e41fc142c931f397ac6420f0f4eabf72954beba0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb7bea28c8f3be597c35991aeefb969726bfa1f08dce062bcb7dfd05f55406e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7df2a0eb61c1b2ac372c144a80e651d08422555bbd264d417afdad46827307(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c73f3450f2944ed30117501bea6207a91346252cb773eff29182b6fe2da016(
    *,
    match_values: typing.Sequence[builtins.str],
    match_variables: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables, typing.Dict[builtins.str, typing.Any]]]],
    operator: builtins.str,
    negation_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98a5bc87db62d1f78dc405c31515707b2c4ca6345cf36f5731d8acbe989cf11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92f43bda64b5e86826e3515b7165f4cf947071c45106c34e78abec737965c7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32a5ea8546b6473d174c26aa0100d14292bdd53c6d85a4e21269c9ecb3f4d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e3d55ca649bb17db12cb4e9e0e601a655c836e6a82bb1e2448aab23232efb0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51dda831f505c5a5033fe3e0d1eac40c11d2dd490db273b3c602d65c9453d524(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645a55f88a73973d3d5850ecbfa10795cfdc54ad2d25b5fbf7b40d9060f34b23(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea398cedb4277c999282f5d0f6e60de6fb225a5433489bfce8435897e910aa89(
    *,
    variable_name: builtins.str,
    selector: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083a6f1459417b6936e2cfbdd205f17a80cbcdf06745d6098569ed8bd0ff727c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4127f00bb170181240150807691fb9ec82ca60feae02614631b1eceb5a26d031(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74d08b30411e886baec5499ba42d48224e7179cacb98164a20572df633b9aea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff6c88b3210de25a9a43db2b5c8709661801540c7c7f5c2e59acb2eca5e093f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9553de99396232f4fda896e79f69ba030a33b9c699be70d4c3f5637d91a66f14(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88d900166f1d8df89878f57489c3df6fcb8ad311bab75665e15e7a7ea5acb6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909dd441e5f0f1851ea51ec5e44964382b1c6006640d563ae33f14a55c2b6384(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b655bbcafcecca6445dcf9197b04e05d56ae54d0cb4fa835c0c6ef1e0a77eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad957fb3fbd8b9219805d68c056d40d0f7d420a4a53d28ea076585cb38e368a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e295e257e3d3fbab7bfd25f12e8300a45bccc3b286a1f77e7482c46fe02e18a5(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc4f2df3320a78fcf2ce57e657f1be12c7a036412af36e2db4202e94f2b8cbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d73b92adc1b3810f5db90ad27cd17162c2e82b4781da8027aa809c41e19ba3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditionsMatchVariables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fcd9488f3a6de325ffe729b482f524fe23c215b06c7602693beb435b79d574(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ca3ac34b643131a5cb5b381c85592ca438194e4a25328039e1990886eafbd0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618b4bc6936bd066382f684d4e8d2865454a933b4c9d7c3665a0b38a03c57f19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c14aa69a740d68282ae7204b862ef0fc7802e7140d1d9cada713311d201d2b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a3dfdcd5a9287f9ae9b58fdd8256fba4fb0b71c863619429458f4a73b8b394(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditions, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c5b7655ecadee89bc5f6d6e243155ed4ccc140bf178557756f0ab6248f617c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a58165d5b271f41dad391a6f786bc99c7bee87631a512734a7fe138cd9f41d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyCustomRulesMatchConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c551a5fe90596ea8dd228222d082becd5c1dda74abfa363f75a4d8c546c82f56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be51241b32b2b8042298611fa8ece10ef189c6a184cd1a5ad14988a68076988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd04fb2683240fc39d1e9d804b8c1aeb8a40f34f7041c25ab56ba2d7b2de933(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1101b0cb63373d766d8706c7f1c2691a47a061b65e0c91d4cdf561cc14162cab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e0c8cd541cc91a8d1d3d185ebe0533bda843d6c2d5356b2fdff555e42dbbde(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyCustomRules, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cc4fc62803753273cb33e670c1da68e19ef01b67231cd938083eed6e02ff97(
    *,
    managed_rule_set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSet, typing.Dict[builtins.str, typing.Any]]]],
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70b68215100175efa2b87cb94f3e890c3c32499a77820d2e8677c48727b432c(
    *,
    match_variable: builtins.str,
    selector: builtins.str,
    selector_match_operator: builtins.str,
    excluded_rule_set: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2030e0236826474a31e23891bf94b91f01c4b3b0f4b0f34e1e6d640f77e3ffe0(
    *,
    rule_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0e94fa767b6f3dcb19653301f0517c1c1027e69800672fab5ab7c8f91fe3e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9806d009c17afbf48b74a4d8e4fcd81f98b6e13a5eff7431f319b0dfb0660dc7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170160d764e50e45a65627e931f64d266f10aa9fc402a533d205c462a3ce543e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b49f31f60be8a2fc5d65d21fa4a222cdbb52e5574e55deb1b5e64b0a373ee2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0a12c815bb9e469617fb84b7fb41900149943968a5ac5bf94216e19b24098e(
    value: typing.Optional[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503b82481225d3a0f8461f4dce7620bba0c07127c8cfe170d5ae80b13eb476e9(
    *,
    rule_group_name: builtins.str,
    excluded_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a276a39e3e8ea536a0d2220d89cf22ac16ad46ad65e599c31e920b41a7ce53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f345de297cd33325a07e002ffc833657edc2a859a9cadb0b9d25e76beef249(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b28722ce8c46a0e7d61f168763d5f922d59684c5a2632c677430d34cbe85381(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f87b31aff2faed6c836e35e5edb38a4bce9e264db911b3ac93b4951465e282b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e560cf2bb2a8ffb1cfe016f20da2352cd8567508edd0e24d23bdf0e8e0ebb2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c74c6fed9e4da6d22d8ea0cab0146a98e86db6d66adc4a9538feecb0608b86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345daa111f3fe85c603d16f1a2385433f9578b1f598af97bc5d59369764c08a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f8929e27c67fce7a4157d1ac57c9d8c71f79ef2ecf67239e67f0db453802d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82afea227f83e75472151f0212fe0582bb1bf713dccaf00dd8d28d8b3219605a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cf264c5d837177e3a817643c4efe522bfb33b91339fb8b0f5793b31f528fc7(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusionExcludedRuleSetRuleGroup, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f90932898c1cb4e70c8ef47a077bfe7614133dd06a4b39982abe3a143ea7fcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d74fed3fc4ea55ac93d87521f5947cba5250e6d9acb4f3ced679608b508d047(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41caf9b08556fc13f5c0d84dbd523a6c2518d2c8df9279e8328a162f4ff9285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1243d77b9efd748bd62d8a19a0e4a657ad0019a5ae3183fe9ed4b88f25edee88(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8111e0b10ce713348b0c1b08a4296d612754519708395889bc6c85a0f10f203(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35dbd1f831e96a422f8eac06d8f80e2fbc0d4c420f4a92ccf170c001bcf2376d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesExclusion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e175f75598d9eb32b13553acd7d18f26432f90931313e899c5b71fd69a613488(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d330385f4186fa21ff9db8b08e9748719cc2676b2510b33a452fa872e2af46c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0c20113c250ca5000ff6f12f78f0fede19ec2094850983ed18fa3bc3bd2326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fd3441066736d7b03d5f4c0cdca345539f245691cf2d1b031631b4ebc9eae8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57313187c06a7cacf494cda3d489205116b617949983e7e823a5f3957e467342(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusion, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2ed48eff12b7310a3ecb0d28aa8683486ada8d18ece389378657482bee885f(
    *,
    version: builtins.str,
    rule_group_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132fec163686efa8ad697d7a2599c78cb1891e4064f310dec662ea6b8c0f41f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669e96bf7bc9992bbb965d33f5bb9b7a288533a69d2f499231b913dad7a4842c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0626a796a6816e4811883866dfe4b827034b6d4d155bbb6c02f91f1bdcb8c579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe571c82b61ce5b8abbebe58a1b7b81c56c916ee09fee40c4a4f55589917f6e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f00ceb1d577e9fd2923f495871d2c438663104e13c18942dab7ef2fcb6ab99(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabcfd894067ca4448948edbedacd9bd43a5d6f1f16b7926375a96366612d67b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa1dc0524d20a97a43ff69ec7ddf9b09ab6b67816ffb3856ed6f6b5549dad94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3b97108df2df9fe04729ff829398728a93c85730c90951ce69846a885e51b1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0478cb6000d7d8a769e7b4767e8cf7165cdabeed13aff2aa2a3fe9b0668f57cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbe07479482f3c638e19440e0e764903e286c18a78466e5ae050f48ec619733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a361572360604fafef8e9958bb99b9ba1f7117760e0a9bb1ab7344a45a1757a7(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSet, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565bbc45342f5657b1e2bb716ca15d5e8f29266bd03e70c94393ff6ce55b669c(
    *,
    rule_group_name: builtins.str,
    disabled_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91428f019523e09551f5fcdbb30ad3e27732367a583290c68c8ed5dcc0bafbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21920fb438c0a6da8f1dcad92f897c7f98842fcccb9f6bd5e1ede6ae57337c1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee72a83a612016fc7e0f1edbd2b5b111e0a74a4da12027a1b9bcb0cb3332afc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348d0969fd3e1fc652f89c3d08293248c57722ba054cf3a5c6d467c54ac05a58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332acbd063f34d0907caec64bd310fe26b1aeb430bface1abe2259fe97c5469d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45cb841b1b4798a8671bc6a16819af3a3de78a3fdd666ec8de87f5ddd167b1ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d085613a12c524a1655a9021103fa76f00b65ef1ac28e89222acc0473704f011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2186422b28e78bbff9f3448c0cf6395262d0103df7ccc38c1cf6599a50c4cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11cbbf77410a7ea0ff5202d9f12b487025b4f56729e938c0fd8352e30512fd5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f92f1d99bd8dc4524b622ae1fa71e0c15ab0a766ee3327585761d3bac23d14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fdbafdd83120b6e9064e910e67691c73ffd7bff5c816f5302eb94d5a9505b0(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverride, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3315631081e2aff3aa78e80ca91322ca8bd3c736265815c1d717aa17d29ea060(
    *,
    id: builtins.str,
    action: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728b4c0434fbae523e360133549cd13c2d08098b8bfcbb5e793b886f60a000a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92abfadd4ddfaf4f582423d4a7fc64121b8daff470165cb7ec627f3eb1324454(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c6cb78ab3f95583867147d6bcbdf7a544f1ad73f92739a019fcee41f06dce2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414bd8377e47d8712ebe6e0c9fe5e6b45fe324d764ba2b90c2c7413a231d78a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df808ee9f1e48b623630ff4ba043f7475adc51c0be3dab5e9fc5248cbd7895e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d240b278e0599697c25ab741a3abe10eb485a467c5be1cbfba9dcd7ef376ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde31467de9dbe9db106247d733fb7bffd27a2073346b02642efa2a0200d0429(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4a2752917672057890d7fe6bd472971e0deba6c3d3b7f97692d32a9714592e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa11ec1a0b1aad6fb9f2a084545f13011a3a28357781d37dfe1e85143a6656ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f679d790754665005be1c05149ec887557698801fbdb5900a0162aacb4cc1666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e406ef60bf78a21c01eda4b9ace8edfa538ea90a0aa9b5d0e2a927059430372(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSetRuleGroupOverrideRule, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dabc846cc38cf79e54f128199399775fb63695094eae04920af1cd099d44d763(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0a611ab3def21f8c094a0444669431914e9659b3537b1cd6504d668c3b33bc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesExclusion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28a1d166dc4b2033064670fc263591939ac519d96198795448d5410a1641633(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebApplicationFirewallPolicyManagedRulesManagedRuleSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493d605c900437f2bcab548a9e697f7e945537b25ae66285b275ddea96ddcb3c(
    value: typing.Optional[WebApplicationFirewallPolicyManagedRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d8810ab0fdf088714565f941f3d9d04e09286411c4c83d6f04807101e90b91(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    file_upload_limit_in_mb: typing.Optional[jsii.Number] = None,
    max_request_body_size_in_kb: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
    request_body_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942c3184a64a4fe9eef9a703f6eb3d14cb979dae8ec1fa7ef4ca37e63205007b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace765a3a2296695c26a4c4d3bfb92bc2e8837e010447648596e4f0af8973c92(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8089efcc73a4a5c5fda5ab3651e04969cc6afb53d55de0299feefa02101847b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebc4ea9759c6e6edb779bb42089e6bd3eb5e8dcaafaa0d1919d86af98e1827c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d0ead72df80e9e994943aa9401105538ce0ada059ef445cd07e211e1a743ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec953f5e203ada9a9618e25b4195ea6ddbdfc2a27860dd8198cd3365ad87adb0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b352f36194865fa8304561959b4dfda2b5a4a095556d250bc6c112b876b9f2(
    value: typing.Optional[WebApplicationFirewallPolicyPolicySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177e788400e574657bb756209d0d909c96d1296975a0e5d7fd5f0646178c9254(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb695d025c665f6855f0dd2edb30e9c1c48126dfe9f4057907432dd8efc349b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca17d34c2deb57dc278db6976afbd486956e2271691efeb5c4f5010e86edc239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a56e002359db65375a6457500c60f95f593deba260c7e010d02258b3d12b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7070dcbb8cd1fc65651b4e80e6c430816d8b8bfbc78e66130280672ac8ff7330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5be38e1628ae9f34795149502cfa557d595cb4a3a429a4bf5a695c67581c91e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4044755143e3c3251666ec3da3d2fdf3e4e96b4d32fc1785d4af9387fca7383(
    value: typing.Optional[typing.Union[WebApplicationFirewallPolicyTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
