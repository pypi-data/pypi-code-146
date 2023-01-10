'''
# `azurerm_logz_monitor`

Refer to the Terraform Registory for docs: [`azurerm_logz_monitor`](https://www.terraform.io/docs/providers/azurerm/r/logz_monitor).
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


class LogzMonitor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logzMonitor.LogzMonitor",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor azurerm_logz_monitor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        plan: typing.Union["LogzMonitorPlan", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        user: typing.Union["LogzMonitorUser", typing.Dict[builtins.str, typing.Any]],
        company_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enterprise_app_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LogzMonitorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor azurerm_logz_monitor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#location LogzMonitor#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#name LogzMonitor#name}.
        :param plan: plan block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#plan LogzMonitor#plan}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#resource_group_name LogzMonitor#resource_group_name}.
        :param user: user block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#user LogzMonitor#user}
        :param company_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#company_name LogzMonitor#company_name}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#enabled LogzMonitor#enabled}.
        :param enterprise_app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#enterprise_app_id LogzMonitor#enterprise_app_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#id LogzMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#tags LogzMonitor#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#timeouts LogzMonitor#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0762988e0718dfddf81319113a0add2c2128ab5fda4285f1ffe304b0bfa92f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LogzMonitorConfig(
            location=location,
            name=name,
            plan=plan,
            resource_group_name=resource_group_name,
            user=user,
            company_name=company_name,
            enabled=enabled,
            enterprise_app_id=enterprise_app_id,
            id=id,
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

    @jsii.member(jsii_name="putPlan")
    def put_plan(
        self,
        *,
        billing_cycle: builtins.str,
        effective_date: builtins.str,
        usage_type: builtins.str,
        plan_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param billing_cycle: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#billing_cycle LogzMonitor#billing_cycle}.
        :param effective_date: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#effective_date LogzMonitor#effective_date}.
        :param usage_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#usage_type LogzMonitor#usage_type}.
        :param plan_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#plan_id LogzMonitor#plan_id}.
        '''
        value = LogzMonitorPlan(
            billing_cycle=billing_cycle,
            effective_date=effective_date,
            usage_type=usage_type,
            plan_id=plan_id,
        )

        return typing.cast(None, jsii.invoke(self, "putPlan", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#create LogzMonitor#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#delete LogzMonitor#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#read LogzMonitor#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#update LogzMonitor#update}.
        '''
        value = LogzMonitorTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUser")
    def put_user(
        self,
        *,
        email: builtins.str,
        first_name: builtins.str,
        last_name: builtins.str,
        phone_number: builtins.str,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#email LogzMonitor#email}.
        :param first_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#first_name LogzMonitor#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#last_name LogzMonitor#last_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#phone_number LogzMonitor#phone_number}.
        '''
        value = LogzMonitorUser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        return typing.cast(None, jsii.invoke(self, "putUser", [value]))

    @jsii.member(jsii_name="resetCompanyName")
    def reset_company_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompanyName", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnterpriseAppId")
    def reset_enterprise_app_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterpriseAppId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="logzOrganizationId")
    def logz_organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logzOrganizationId"))

    @builtins.property
    @jsii.member(jsii_name="plan")
    def plan(self) -> "LogzMonitorPlanOutputReference":
        return typing.cast("LogzMonitorPlanOutputReference", jsii.get(self, "plan"))

    @builtins.property
    @jsii.member(jsii_name="singleSignOnUrl")
    def single_sign_on_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleSignOnUrl"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LogzMonitorTimeoutsOutputReference":
        return typing.cast("LogzMonitorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> "LogzMonitorUserOutputReference":
        return typing.cast("LogzMonitorUserOutputReference", jsii.get(self, "user"))

    @builtins.property
    @jsii.member(jsii_name="companyNameInput")
    def company_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "companyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseAppIdInput")
    def enterprise_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="planInput")
    def plan_input(self) -> typing.Optional["LogzMonitorPlan"]:
        return typing.cast(typing.Optional["LogzMonitorPlan"], jsii.get(self, "planInput"))

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
    ) -> typing.Optional[typing.Union["LogzMonitorTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["LogzMonitorTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional["LogzMonitorUser"]:
        return typing.cast(typing.Optional["LogzMonitorUser"], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="companyName")
    def company_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "companyName"))

    @company_name.setter
    def company_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede0839af510c04db659238390179e39ee39e9f0fc91f3d571d127ce75a9e93d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__fb10d014e6f5d19da23b5c40a9c7043fd4d89c5a8a0701b79e768524f239a5c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="enterpriseAppId")
    def enterprise_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseAppId"))

    @enterprise_app_id.setter
    def enterprise_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3dc3a57acf0bce0f29ab4109f61a4e8f0872a000b3b2dc5785bd65305302e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseAppId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c639d3ff0f80635e833454c077b833164cea372aaf5ab5c7dfc150fc1cdf43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622ec2d3b4efb4da760182267b2fc8be076f399489d0d6f1502b80a8b7817ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee7c234396c0b73d9792b30dcc684d3ad76dbe24974a016a882d327f7b9880c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d176a47560578569e2c7bf9fe58f561f65d6c4f8bc70a1967179e73a27b3c6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30eaa6cdb27fb2278303da40fdf24a16b1d29f273867cfe532d87b23e01a32f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logzMonitor.LogzMonitorConfig",
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
        "name": "name",
        "plan": "plan",
        "resource_group_name": "resourceGroupName",
        "user": "user",
        "company_name": "companyName",
        "enabled": "enabled",
        "enterprise_app_id": "enterpriseAppId",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class LogzMonitorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        plan: typing.Union["LogzMonitorPlan", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        user: typing.Union["LogzMonitorUser", typing.Dict[builtins.str, typing.Any]],
        company_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enterprise_app_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LogzMonitorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#location LogzMonitor#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#name LogzMonitor#name}.
        :param plan: plan block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#plan LogzMonitor#plan}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#resource_group_name LogzMonitor#resource_group_name}.
        :param user: user block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#user LogzMonitor#user}
        :param company_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#company_name LogzMonitor#company_name}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#enabled LogzMonitor#enabled}.
        :param enterprise_app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#enterprise_app_id LogzMonitor#enterprise_app_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#id LogzMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#tags LogzMonitor#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#timeouts LogzMonitor#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(plan, dict):
            plan = LogzMonitorPlan(**plan)
        if isinstance(user, dict):
            user = LogzMonitorUser(**user)
        if isinstance(timeouts, dict):
            timeouts = LogzMonitorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4e486ab005ed81eca7cd9f9050587834438ba807da00b108e69a04e637e909)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enterprise_app_id", value=enterprise_app_id, expected_type=type_hints["enterprise_app_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "plan": plan,
            "resource_group_name": resource_group_name,
            "user": user,
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
        if company_name is not None:
            self._values["company_name"] = company_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if enterprise_app_id is not None:
            self._values["enterprise_app_id"] = enterprise_app_id
        if id is not None:
            self._values["id"] = id
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#location LogzMonitor#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#name LogzMonitor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plan(self) -> "LogzMonitorPlan":
        '''plan block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#plan LogzMonitor#plan}
        '''
        result = self._values.get("plan")
        assert result is not None, "Required property 'plan' is missing"
        return typing.cast("LogzMonitorPlan", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#resource_group_name LogzMonitor#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> "LogzMonitorUser":
        '''user block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#user LogzMonitor#user}
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast("LogzMonitorUser", result)

    @builtins.property
    def company_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#company_name LogzMonitor#company_name}.'''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#enabled LogzMonitor#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enterprise_app_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#enterprise_app_id LogzMonitor#enterprise_app_id}.'''
        result = self._values.get("enterprise_app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#id LogzMonitor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#tags LogzMonitor#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LogzMonitorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#timeouts LogzMonitor#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LogzMonitorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogzMonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logzMonitor.LogzMonitorPlan",
    jsii_struct_bases=[],
    name_mapping={
        "billing_cycle": "billingCycle",
        "effective_date": "effectiveDate",
        "usage_type": "usageType",
        "plan_id": "planId",
    },
)
class LogzMonitorPlan:
    def __init__(
        self,
        *,
        billing_cycle: builtins.str,
        effective_date: builtins.str,
        usage_type: builtins.str,
        plan_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param billing_cycle: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#billing_cycle LogzMonitor#billing_cycle}.
        :param effective_date: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#effective_date LogzMonitor#effective_date}.
        :param usage_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#usage_type LogzMonitor#usage_type}.
        :param plan_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#plan_id LogzMonitor#plan_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b675da379811ce6cc02595021ec0ff98d40b725399e858990b84c84c2d5289b5)
            check_type(argname="argument billing_cycle", value=billing_cycle, expected_type=type_hints["billing_cycle"])
            check_type(argname="argument effective_date", value=effective_date, expected_type=type_hints["effective_date"])
            check_type(argname="argument usage_type", value=usage_type, expected_type=type_hints["usage_type"])
            check_type(argname="argument plan_id", value=plan_id, expected_type=type_hints["plan_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "billing_cycle": billing_cycle,
            "effective_date": effective_date,
            "usage_type": usage_type,
        }
        if plan_id is not None:
            self._values["plan_id"] = plan_id

    @builtins.property
    def billing_cycle(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#billing_cycle LogzMonitor#billing_cycle}.'''
        result = self._values.get("billing_cycle")
        assert result is not None, "Required property 'billing_cycle' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def effective_date(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#effective_date LogzMonitor#effective_date}.'''
        result = self._values.get("effective_date")
        assert result is not None, "Required property 'effective_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def usage_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#usage_type LogzMonitor#usage_type}.'''
        result = self._values.get("usage_type")
        assert result is not None, "Required property 'usage_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plan_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#plan_id LogzMonitor#plan_id}.'''
        result = self._values.get("plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogzMonitorPlan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogzMonitorPlanOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logzMonitor.LogzMonitorPlanOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76ca89f846f5d11b87b0bc1dcf5beb3cb6f3b67df379b718613bef6273aa6be4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPlanId")
    def reset_plan_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlanId", []))

    @builtins.property
    @jsii.member(jsii_name="billingCycleInput")
    def billing_cycle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingCycleInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveDateInput")
    def effective_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveDateInput"))

    @builtins.property
    @jsii.member(jsii_name="planIdInput")
    def plan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "planIdInput"))

    @builtins.property
    @jsii.member(jsii_name="usageTypeInput")
    def usage_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="billingCycle")
    def billing_cycle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingCycle"))

    @billing_cycle.setter
    def billing_cycle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d588fce3f2f20000d74b02e0739a07e6ab72884eee8b7ea06aa0f4f3d7388e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingCycle", value)

    @builtins.property
    @jsii.member(jsii_name="effectiveDate")
    def effective_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveDate"))

    @effective_date.setter
    def effective_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053d16bb8933e22ed717fc1375057a7ff4d941f52010e187aba63b3151b5199d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveDate", value)

    @builtins.property
    @jsii.member(jsii_name="planId")
    def plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "planId"))

    @plan_id.setter
    def plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03859007099a7f6f78aa2acaafc25e755676c8900502ffa715d497d7bd5117f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "planId", value)

    @builtins.property
    @jsii.member(jsii_name="usageType")
    def usage_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usageType"))

    @usage_type.setter
    def usage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de1053057943a418ae77da0e272aae453674425dc0f590fcea8a2b5b103bee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usageType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogzMonitorPlan]:
        return typing.cast(typing.Optional[LogzMonitorPlan], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogzMonitorPlan]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6e3d2fd4ba968f4a6e364285af4dc3c92f9fee02f7ba340322a14ec9de6fcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logzMonitor.LogzMonitorTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class LogzMonitorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#create LogzMonitor#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#delete LogzMonitor#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#read LogzMonitor#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#update LogzMonitor#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7813afedd5a8116b9efd8375dd2fa378f236bc6d091863059d4ab2e71f53dba5)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#create LogzMonitor#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#delete LogzMonitor#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#read LogzMonitor#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#update LogzMonitor#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogzMonitorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogzMonitorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logzMonitor.LogzMonitorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82a0815e8a5e6ce0daa70885d45cbb65e6e1d36d036d1c84d507895a79ffaf78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3bc66c9142a8e27b27805bb93e0905c44edbf8fab215753d07da7f34c6f6cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502acd40f3c52bf4ef6a330986671aca298bbd5cb710c791fdfca42783cca6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aff699df8d740c14025a485834b24eeb325c9fb8ec96ae670bccab90acd50b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c9ce71dd680daa225b3b1ebb4586aa453aff23bae6156718d6a15cb2031492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LogzMonitorTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LogzMonitorTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LogzMonitorTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9cd82e673d65864ce0bd8ade99054e1dbf2e3ea692043cbd57a63f54f0e1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logzMonitor.LogzMonitorUser",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "first_name": "firstName",
        "last_name": "lastName",
        "phone_number": "phoneNumber",
    },
)
class LogzMonitorUser:
    def __init__(
        self,
        *,
        email: builtins.str,
        first_name: builtins.str,
        last_name: builtins.str,
        phone_number: builtins.str,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#email LogzMonitor#email}.
        :param first_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#first_name LogzMonitor#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#last_name LogzMonitor#last_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#phone_number LogzMonitor#phone_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f1fd2b7d0fd724f4c18440c61c8e8d35f014c876c79d061d6654c469957e7c)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
        }

    @builtins.property
    def email(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#email LogzMonitor#email}.'''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def first_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#first_name LogzMonitor#first_name}.'''
        result = self._values.get("first_name")
        assert result is not None, "Required property 'first_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def last_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#last_name LogzMonitor#last_name}.'''
        result = self._values.get("last_name")
        assert result is not None, "Required property 'last_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/logz_monitor#phone_number LogzMonitor#phone_number}.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogzMonitorUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogzMonitorUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logzMonitor.LogzMonitorUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ed29d9824e226da8859e95bb4ed461deddf573bfb36ed9dd1fd22a46638811f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74b9a9202dd0bf15f96b7e7ec60752a286604cafa87278f9464714c8b283af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15553414707ce62c853d5d3c000c667f0410b53bab687bc80c46a5e5a55a3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value)

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6651ca24faff782e1f0fdf4f2d8524eef243538ab0e04bc0e73c9eb2a83e498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value)

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe197d5102dec56f16b015856b3ff42d7ff17d0002806440c1b1c8404f55a72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogzMonitorUser]:
        return typing.cast(typing.Optional[LogzMonitorUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogzMonitorUser]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9bc96d21d11c86d0fa8bee4741dc0de00ddd551d5d24ab047ede155ece99871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LogzMonitor",
    "LogzMonitorConfig",
    "LogzMonitorPlan",
    "LogzMonitorPlanOutputReference",
    "LogzMonitorTimeouts",
    "LogzMonitorTimeoutsOutputReference",
    "LogzMonitorUser",
    "LogzMonitorUserOutputReference",
]

publication.publish()

def _typecheckingstub__eb0762988e0718dfddf81319113a0add2c2128ab5fda4285f1ffe304b0bfa92f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    plan: typing.Union[LogzMonitorPlan, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    user: typing.Union[LogzMonitorUser, typing.Dict[builtins.str, typing.Any]],
    company_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enterprise_app_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LogzMonitorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ede0839af510c04db659238390179e39ee39e9f0fc91f3d571d127ce75a9e93d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb10d014e6f5d19da23b5c40a9c7043fd4d89c5a8a0701b79e768524f239a5c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3dc3a57acf0bce0f29ab4109f61a4e8f0872a000b3b2dc5785bd65305302e33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c639d3ff0f80635e833454c077b833164cea372aaf5ab5c7dfc150fc1cdf43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622ec2d3b4efb4da760182267b2fc8be076f399489d0d6f1502b80a8b7817ff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee7c234396c0b73d9792b30dcc684d3ad76dbe24974a016a882d327f7b9880c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d176a47560578569e2c7bf9fe58f561f65d6c4f8bc70a1967179e73a27b3c6c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30eaa6cdb27fb2278303da40fdf24a16b1d29f273867cfe532d87b23e01a32f2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4e486ab005ed81eca7cd9f9050587834438ba807da00b108e69a04e637e909(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    plan: typing.Union[LogzMonitorPlan, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    user: typing.Union[LogzMonitorUser, typing.Dict[builtins.str, typing.Any]],
    company_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enterprise_app_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LogzMonitorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b675da379811ce6cc02595021ec0ff98d40b725399e858990b84c84c2d5289b5(
    *,
    billing_cycle: builtins.str,
    effective_date: builtins.str,
    usage_type: builtins.str,
    plan_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ca89f846f5d11b87b0bc1dcf5beb3cb6f3b67df379b718613bef6273aa6be4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d588fce3f2f20000d74b02e0739a07e6ab72884eee8b7ea06aa0f4f3d7388e50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053d16bb8933e22ed717fc1375057a7ff4d941f52010e187aba63b3151b5199d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03859007099a7f6f78aa2acaafc25e755676c8900502ffa715d497d7bd5117f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de1053057943a418ae77da0e272aae453674425dc0f590fcea8a2b5b103bee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6e3d2fd4ba968f4a6e364285af4dc3c92f9fee02f7ba340322a14ec9de6fcc(
    value: typing.Optional[LogzMonitorPlan],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7813afedd5a8116b9efd8375dd2fa378f236bc6d091863059d4ab2e71f53dba5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a0815e8a5e6ce0daa70885d45cbb65e6e1d36d036d1c84d507895a79ffaf78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bc66c9142a8e27b27805bb93e0905c44edbf8fab215753d07da7f34c6f6cd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502acd40f3c52bf4ef6a330986671aca298bbd5cb710c791fdfca42783cca6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aff699df8d740c14025a485834b24eeb325c9fb8ec96ae670bccab90acd50b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c9ce71dd680daa225b3b1ebb4586aa453aff23bae6156718d6a15cb2031492(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9cd82e673d65864ce0bd8ade99054e1dbf2e3ea692043cbd57a63f54f0e1d4(
    value: typing.Optional[typing.Union[LogzMonitorTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f1fd2b7d0fd724f4c18440c61c8e8d35f014c876c79d061d6654c469957e7c(
    *,
    email: builtins.str,
    first_name: builtins.str,
    last_name: builtins.str,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed29d9824e226da8859e95bb4ed461deddf573bfb36ed9dd1fd22a46638811f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74b9a9202dd0bf15f96b7e7ec60752a286604cafa87278f9464714c8b283af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15553414707ce62c853d5d3c000c667f0410b53bab687bc80c46a5e5a55a3b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6651ca24faff782e1f0fdf4f2d8524eef243538ab0e04bc0e73c9eb2a83e498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe197d5102dec56f16b015856b3ff42d7ff17d0002806440c1b1c8404f55a72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bc96d21d11c86d0fa8bee4741dc0de00ddd551d5d24ab047ede155ece99871(
    value: typing.Optional[LogzMonitorUser],
) -> None:
    """Type checking stubs"""
    pass
