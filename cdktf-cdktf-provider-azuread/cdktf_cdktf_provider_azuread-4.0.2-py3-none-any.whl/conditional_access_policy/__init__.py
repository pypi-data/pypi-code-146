'''
# `azuread_conditional_access_policy`

Refer to the Terraform Registory for docs: [`azuread_conditional_access_policy`](https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy).
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


class ConditionalAccessPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy azuread_conditional_access_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        conditions: typing.Union["ConditionalAccessPolicyConditions", typing.Dict[builtins.str, typing.Any]],
        display_name: builtins.str,
        grant_controls: typing.Union["ConditionalAccessPolicyGrantControls", typing.Dict[builtins.str, typing.Any]],
        state: builtins.str,
        id: typing.Optional[builtins.str] = None,
        session_controls: typing.Optional[typing.Union["ConditionalAccessPolicySessionControls", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ConditionalAccessPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy azuread_conditional_access_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#conditions ConditionalAccessPolicy#conditions}
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#display_name ConditionalAccessPolicy#display_name}.
        :param grant_controls: grant_controls block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#grant_controls ConditionalAccessPolicy#grant_controls}
        :param state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#state ConditionalAccessPolicy#state}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#id ConditionalAccessPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param session_controls: session_controls block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#session_controls ConditionalAccessPolicy#session_controls}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#timeouts ConditionalAccessPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda8e7441b6c17a94a8f11203cb1e09fdd85e21778b3a7504886befd5467b549)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ConditionalAccessPolicyConfig(
            conditions=conditions,
            display_name=display_name,
            grant_controls=grant_controls,
            state=state,
            id=id,
            session_controls=session_controls,
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

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        applications: typing.Union["ConditionalAccessPolicyConditionsApplications", typing.Dict[builtins.str, typing.Any]],
        client_app_types: typing.Sequence[builtins.str],
        users: typing.Union["ConditionalAccessPolicyConditionsUsers", typing.Dict[builtins.str, typing.Any]],
        devices: typing.Optional[typing.Union["ConditionalAccessPolicyConditionsDevices", typing.Dict[builtins.str, typing.Any]]] = None,
        locations: typing.Optional[typing.Union["ConditionalAccessPolicyConditionsLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        platforms: typing.Optional[typing.Union["ConditionalAccessPolicyConditionsPlatforms", typing.Dict[builtins.str, typing.Any]]] = None,
        sign_in_risk_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_risk_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param applications: applications block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#applications ConditionalAccessPolicy#applications}
        :param client_app_types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#client_app_types ConditionalAccessPolicy#client_app_types}.
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#users ConditionalAccessPolicy#users}
        :param devices: devices block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#devices ConditionalAccessPolicy#devices}
        :param locations: locations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#locations ConditionalAccessPolicy#locations}
        :param platforms: platforms block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#platforms ConditionalAccessPolicy#platforms}
        :param sign_in_risk_levels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_risk_levels ConditionalAccessPolicy#sign_in_risk_levels}.
        :param user_risk_levels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#user_risk_levels ConditionalAccessPolicy#user_risk_levels}.
        '''
        value = ConditionalAccessPolicyConditions(
            applications=applications,
            client_app_types=client_app_types,
            users=users,
            devices=devices,
            locations=locations,
            platforms=platforms,
            sign_in_risk_levels=sign_in_risk_levels,
            user_risk_levels=user_risk_levels,
        )

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putGrantControls")
    def put_grant_controls(
        self,
        *,
        built_in_controls: typing.Sequence[builtins.str],
        operator: builtins.str,
        custom_authentication_factors: typing.Optional[typing.Sequence[builtins.str]] = None,
        terms_of_use: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param built_in_controls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#built_in_controls ConditionalAccessPolicy#built_in_controls}.
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#operator ConditionalAccessPolicy#operator}.
        :param custom_authentication_factors: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#custom_authentication_factors ConditionalAccessPolicy#custom_authentication_factors}.
        :param terms_of_use: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#terms_of_use ConditionalAccessPolicy#terms_of_use}.
        '''
        value = ConditionalAccessPolicyGrantControls(
            built_in_controls=built_in_controls,
            operator=operator,
            custom_authentication_factors=custom_authentication_factors,
            terms_of_use=terms_of_use,
        )

        return typing.cast(None, jsii.invoke(self, "putGrantControls", [value]))

    @jsii.member(jsii_name="putSessionControls")
    def put_session_controls(
        self,
        *,
        application_enforced_restrictions_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cloud_app_security_policy: typing.Optional[builtins.str] = None,
        persistent_browser_mode: typing.Optional[builtins.str] = None,
        sign_in_frequency: typing.Optional[jsii.Number] = None,
        sign_in_frequency_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_enforced_restrictions_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#application_enforced_restrictions_enabled ConditionalAccessPolicy#application_enforced_restrictions_enabled}.
        :param cloud_app_security_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#cloud_app_security_policy ConditionalAccessPolicy#cloud_app_security_policy}.
        :param persistent_browser_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#persistent_browser_mode ConditionalAccessPolicy#persistent_browser_mode}.
        :param sign_in_frequency: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_frequency ConditionalAccessPolicy#sign_in_frequency}.
        :param sign_in_frequency_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_frequency_period ConditionalAccessPolicy#sign_in_frequency_period}.
        '''
        value = ConditionalAccessPolicySessionControls(
            application_enforced_restrictions_enabled=application_enforced_restrictions_enabled,
            cloud_app_security_policy=cloud_app_security_policy,
            persistent_browser_mode=persistent_browser_mode,
            sign_in_frequency=sign_in_frequency,
            sign_in_frequency_period=sign_in_frequency_period,
        )

        return typing.cast(None, jsii.invoke(self, "putSessionControls", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#create ConditionalAccessPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#delete ConditionalAccessPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#read ConditionalAccessPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#update ConditionalAccessPolicy#update}.
        '''
        value = ConditionalAccessPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSessionControls")
    def reset_session_controls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionControls", []))

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
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "ConditionalAccessPolicyConditionsOutputReference":
        return typing.cast("ConditionalAccessPolicyConditionsOutputReference", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="grantControls")
    def grant_controls(self) -> "ConditionalAccessPolicyGrantControlsOutputReference":
        return typing.cast("ConditionalAccessPolicyGrantControlsOutputReference", jsii.get(self, "grantControls"))

    @builtins.property
    @jsii.member(jsii_name="sessionControls")
    def session_controls(
        self,
    ) -> "ConditionalAccessPolicySessionControlsOutputReference":
        return typing.cast("ConditionalAccessPolicySessionControlsOutputReference", jsii.get(self, "sessionControls"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ConditionalAccessPolicyTimeoutsOutputReference":
        return typing.cast("ConditionalAccessPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(self) -> typing.Optional["ConditionalAccessPolicyConditions"]:
        return typing.cast(typing.Optional["ConditionalAccessPolicyConditions"], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="grantControlsInput")
    def grant_controls_input(
        self,
    ) -> typing.Optional["ConditionalAccessPolicyGrantControls"]:
        return typing.cast(typing.Optional["ConditionalAccessPolicyGrantControls"], jsii.get(self, "grantControlsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionControlsInput")
    def session_controls_input(
        self,
    ) -> typing.Optional["ConditionalAccessPolicySessionControls"]:
        return typing.cast(typing.Optional["ConditionalAccessPolicySessionControls"], jsii.get(self, "sessionControlsInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["ConditionalAccessPolicyTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ConditionalAccessPolicyTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d18a0404f165bfdb4ea8c14882156509c53466357b61d759c2143265947f45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342ac25be951f7194888f7ba4e2320e9df9c00d0cb3abe1617379409f9d2c951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90be1c5002ea4b6b68e2c267c3c472c2dc471b8a056dfe9c31891d1c80d536fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditions",
    jsii_struct_bases=[],
    name_mapping={
        "applications": "applications",
        "client_app_types": "clientAppTypes",
        "users": "users",
        "devices": "devices",
        "locations": "locations",
        "platforms": "platforms",
        "sign_in_risk_levels": "signInRiskLevels",
        "user_risk_levels": "userRiskLevels",
    },
)
class ConditionalAccessPolicyConditions:
    def __init__(
        self,
        *,
        applications: typing.Union["ConditionalAccessPolicyConditionsApplications", typing.Dict[builtins.str, typing.Any]],
        client_app_types: typing.Sequence[builtins.str],
        users: typing.Union["ConditionalAccessPolicyConditionsUsers", typing.Dict[builtins.str, typing.Any]],
        devices: typing.Optional[typing.Union["ConditionalAccessPolicyConditionsDevices", typing.Dict[builtins.str, typing.Any]]] = None,
        locations: typing.Optional[typing.Union["ConditionalAccessPolicyConditionsLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        platforms: typing.Optional[typing.Union["ConditionalAccessPolicyConditionsPlatforms", typing.Dict[builtins.str, typing.Any]]] = None,
        sign_in_risk_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_risk_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param applications: applications block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#applications ConditionalAccessPolicy#applications}
        :param client_app_types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#client_app_types ConditionalAccessPolicy#client_app_types}.
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#users ConditionalAccessPolicy#users}
        :param devices: devices block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#devices ConditionalAccessPolicy#devices}
        :param locations: locations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#locations ConditionalAccessPolicy#locations}
        :param platforms: platforms block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#platforms ConditionalAccessPolicy#platforms}
        :param sign_in_risk_levels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_risk_levels ConditionalAccessPolicy#sign_in_risk_levels}.
        :param user_risk_levels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#user_risk_levels ConditionalAccessPolicy#user_risk_levels}.
        '''
        if isinstance(applications, dict):
            applications = ConditionalAccessPolicyConditionsApplications(**applications)
        if isinstance(users, dict):
            users = ConditionalAccessPolicyConditionsUsers(**users)
        if isinstance(devices, dict):
            devices = ConditionalAccessPolicyConditionsDevices(**devices)
        if isinstance(locations, dict):
            locations = ConditionalAccessPolicyConditionsLocations(**locations)
        if isinstance(platforms, dict):
            platforms = ConditionalAccessPolicyConditionsPlatforms(**platforms)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6ca498f70a8dfc5ca12bb3ca3b60ed0decb89bca1f16d3eb3835416a5c6355)
            check_type(argname="argument applications", value=applications, expected_type=type_hints["applications"])
            check_type(argname="argument client_app_types", value=client_app_types, expected_type=type_hints["client_app_types"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument platforms", value=platforms, expected_type=type_hints["platforms"])
            check_type(argname="argument sign_in_risk_levels", value=sign_in_risk_levels, expected_type=type_hints["sign_in_risk_levels"])
            check_type(argname="argument user_risk_levels", value=user_risk_levels, expected_type=type_hints["user_risk_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "applications": applications,
            "client_app_types": client_app_types,
            "users": users,
        }
        if devices is not None:
            self._values["devices"] = devices
        if locations is not None:
            self._values["locations"] = locations
        if platforms is not None:
            self._values["platforms"] = platforms
        if sign_in_risk_levels is not None:
            self._values["sign_in_risk_levels"] = sign_in_risk_levels
        if user_risk_levels is not None:
            self._values["user_risk_levels"] = user_risk_levels

    @builtins.property
    def applications(self) -> "ConditionalAccessPolicyConditionsApplications":
        '''applications block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#applications ConditionalAccessPolicy#applications}
        '''
        result = self._values.get("applications")
        assert result is not None, "Required property 'applications' is missing"
        return typing.cast("ConditionalAccessPolicyConditionsApplications", result)

    @builtins.property
    def client_app_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#client_app_types ConditionalAccessPolicy#client_app_types}.'''
        result = self._values.get("client_app_types")
        assert result is not None, "Required property 'client_app_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def users(self) -> "ConditionalAccessPolicyConditionsUsers":
        '''users block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#users ConditionalAccessPolicy#users}
        '''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast("ConditionalAccessPolicyConditionsUsers", result)

    @builtins.property
    def devices(self) -> typing.Optional["ConditionalAccessPolicyConditionsDevices"]:
        '''devices block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#devices ConditionalAccessPolicy#devices}
        '''
        result = self._values.get("devices")
        return typing.cast(typing.Optional["ConditionalAccessPolicyConditionsDevices"], result)

    @builtins.property
    def locations(
        self,
    ) -> typing.Optional["ConditionalAccessPolicyConditionsLocations"]:
        '''locations block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#locations ConditionalAccessPolicy#locations}
        '''
        result = self._values.get("locations")
        return typing.cast(typing.Optional["ConditionalAccessPolicyConditionsLocations"], result)

    @builtins.property
    def platforms(
        self,
    ) -> typing.Optional["ConditionalAccessPolicyConditionsPlatforms"]:
        '''platforms block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#platforms ConditionalAccessPolicy#platforms}
        '''
        result = self._values.get("platforms")
        return typing.cast(typing.Optional["ConditionalAccessPolicyConditionsPlatforms"], result)

    @builtins.property
    def sign_in_risk_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_risk_levels ConditionalAccessPolicy#sign_in_risk_levels}.'''
        result = self._values.get("sign_in_risk_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_risk_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#user_risk_levels ConditionalAccessPolicy#user_risk_levels}.'''
        result = self._values.get("user_risk_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsApplications",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_applications": "excludedApplications",
        "included_applications": "includedApplications",
        "included_user_actions": "includedUserActions",
    },
)
class ConditionalAccessPolicyConditionsApplications:
    def __init__(
        self,
        *,
        excluded_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_user_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excluded_applications: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_applications ConditionalAccessPolicy#excluded_applications}.
        :param included_applications: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_applications ConditionalAccessPolicy#included_applications}.
        :param included_user_actions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_user_actions ConditionalAccessPolicy#included_user_actions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11026c77806c5638ff31deed764671983442729eab6de259f981e4c908541f3d)
            check_type(argname="argument excluded_applications", value=excluded_applications, expected_type=type_hints["excluded_applications"])
            check_type(argname="argument included_applications", value=included_applications, expected_type=type_hints["included_applications"])
            check_type(argname="argument included_user_actions", value=included_user_actions, expected_type=type_hints["included_user_actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excluded_applications is not None:
            self._values["excluded_applications"] = excluded_applications
        if included_applications is not None:
            self._values["included_applications"] = included_applications
        if included_user_actions is not None:
            self._values["included_user_actions"] = included_user_actions

    @builtins.property
    def excluded_applications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_applications ConditionalAccessPolicy#excluded_applications}.'''
        result = self._values.get("excluded_applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_applications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_applications ConditionalAccessPolicy#included_applications}.'''
        result = self._values.get("included_applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_user_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_user_actions ConditionalAccessPolicy#included_user_actions}.'''
        result = self._values.get("included_user_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyConditionsApplications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalAccessPolicyConditionsApplicationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsApplicationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44a676bd53c40d07330145257c71816fe95b1d855afa31f76b0863a0a2792019)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedApplications")
    def reset_excluded_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedApplications", []))

    @jsii.member(jsii_name="resetIncludedApplications")
    def reset_included_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedApplications", []))

    @jsii.member(jsii_name="resetIncludedUserActions")
    def reset_included_user_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedUserActions", []))

    @builtins.property
    @jsii.member(jsii_name="excludedApplicationsInput")
    def excluded_applications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedApplicationsInput")
    def included_applications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedUserActionsInput")
    def included_user_actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedUserActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedApplications")
    def excluded_applications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedApplications"))

    @excluded_applications.setter
    def excluded_applications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ab46b5507641840d8949499b472c6c92ed035112342750e5c4889d634d7f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedApplications", value)

    @builtins.property
    @jsii.member(jsii_name="includedApplications")
    def included_applications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedApplications"))

    @included_applications.setter
    def included_applications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e839be7313e78c97bf4138370ee51df87bb1341610ccd0e80322fc16437e3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedApplications", value)

    @builtins.property
    @jsii.member(jsii_name="includedUserActions")
    def included_user_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedUserActions"))

    @included_user_actions.setter
    def included_user_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a4e85ea0367fc0583aa794febc9e3cde4c69679e8d175d19539454f376f34a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedUserActions", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsApplications]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsApplications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicyConditionsApplications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d941fe07358af071bdf274dda21da709cf19acea868060a88b5e138936d784a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsDevices",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class ConditionalAccessPolicyConditionsDevices:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union["ConditionalAccessPolicyConditionsDevicesFilter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#filter ConditionalAccessPolicy#filter}
        '''
        if isinstance(filter, dict):
            filter = ConditionalAccessPolicyConditionsDevicesFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10c350974ac5d12ae2af28f283d7438255f38b9521f79e8b6f4eced175ce5cf)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["ConditionalAccessPolicyConditionsDevicesFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#filter ConditionalAccessPolicy#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["ConditionalAccessPolicyConditionsDevicesFilter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyConditionsDevices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsDevicesFilter",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "rule": "rule"},
)
class ConditionalAccessPolicyConditionsDevicesFilter:
    def __init__(self, *, mode: builtins.str, rule: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#mode ConditionalAccessPolicy#mode}.
        :param rule: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#rule ConditionalAccessPolicy#rule}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ef6a53b1c5c09838967f0d12f8571d12ff78e2108dfcac619ea0b0cd24911b)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "rule": rule,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#mode ConditionalAccessPolicy#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#rule ConditionalAccessPolicy#rule}.'''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyConditionsDevicesFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalAccessPolicyConditionsDevicesFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsDevicesFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ecb07c2222332c25d550601fd14f2c0dca72cd0070180f4dbac9e643e41218b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebad9b002ea036162bbadde106cb69e4570429b663c426366e849ca6e9455ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37d0569adba8fbef8f8f465fb188a4d5e698f89903589abbf79f6a55850810b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsDevicesFilter]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsDevicesFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicyConditionsDevicesFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3977248f725b9010cef3cc316c56c9467452bc0efdb66cf9daa757267a73563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ConditionalAccessPolicyConditionsDevicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsDevicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fe3b86180f822c41519d6f4bb6370130051e114607799ae0c5cde1044c00c7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(self, *, mode: builtins.str, rule: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#mode ConditionalAccessPolicy#mode}.
        :param rule: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#rule ConditionalAccessPolicy#rule}.
        '''
        value = ConditionalAccessPolicyConditionsDevicesFilter(mode=mode, rule=rule)

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> ConditionalAccessPolicyConditionsDevicesFilterOutputReference:
        return typing.cast(ConditionalAccessPolicyConditionsDevicesFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsDevicesFilter]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsDevicesFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsDevices]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsDevices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicyConditionsDevices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1829bc397b7f24258976851673507c9eb6333f185381c2e2c6b61eab3aeff732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsLocations",
    jsii_struct_bases=[],
    name_mapping={
        "included_locations": "includedLocations",
        "excluded_locations": "excludedLocations",
    },
)
class ConditionalAccessPolicyConditionsLocations:
    def __init__(
        self,
        *,
        included_locations: typing.Sequence[builtins.str],
        excluded_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_locations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_locations ConditionalAccessPolicy#included_locations}.
        :param excluded_locations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_locations ConditionalAccessPolicy#excluded_locations}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c7305eb364afef5b292e50c63c9b45344be7eb5e3a26e450df5391eb9c959e)
            check_type(argname="argument included_locations", value=included_locations, expected_type=type_hints["included_locations"])
            check_type(argname="argument excluded_locations", value=excluded_locations, expected_type=type_hints["excluded_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "included_locations": included_locations,
        }
        if excluded_locations is not None:
            self._values["excluded_locations"] = excluded_locations

    @builtins.property
    def included_locations(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_locations ConditionalAccessPolicy#included_locations}.'''
        result = self._values.get("included_locations")
        assert result is not None, "Required property 'included_locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def excluded_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_locations ConditionalAccessPolicy#excluded_locations}.'''
        result = self._values.get("excluded_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyConditionsLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalAccessPolicyConditionsLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cfa937160d76f86e7e6d239a2e3bae1ac2edafbe66b41da9cb51a4dfdc17fdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedLocations")
    def reset_excluded_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedLocations", []))

    @builtins.property
    @jsii.member(jsii_name="excludedLocationsInput")
    def excluded_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedLocationsInput")
    def included_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedLocations")
    def excluded_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedLocations"))

    @excluded_locations.setter
    def excluded_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a8fc9de65b1c675b9903c72212e0af17a6a6652fb88606f9f42697cb35f3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedLocations", value)

    @builtins.property
    @jsii.member(jsii_name="includedLocations")
    def included_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedLocations"))

    @included_locations.setter
    def included_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64dfcd9642f63298175cef996acc07af6e466cf67a219b06cf4f5200ca700e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedLocations", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsLocations]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicyConditionsLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11347f7b2296191f5aefe02b8031b7e47a87bd5da8a12937bff31101a6a78d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ConditionalAccessPolicyConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb8d93a80edffae6b02ed055a4fa9d61f3439be406e051d81fc0b1f62464e1f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApplications")
    def put_applications(
        self,
        *,
        excluded_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_user_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excluded_applications: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_applications ConditionalAccessPolicy#excluded_applications}.
        :param included_applications: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_applications ConditionalAccessPolicy#included_applications}.
        :param included_user_actions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_user_actions ConditionalAccessPolicy#included_user_actions}.
        '''
        value = ConditionalAccessPolicyConditionsApplications(
            excluded_applications=excluded_applications,
            included_applications=included_applications,
            included_user_actions=included_user_actions,
        )

        return typing.cast(None, jsii.invoke(self, "putApplications", [value]))

    @jsii.member(jsii_name="putDevices")
    def put_devices(
        self,
        *,
        filter: typing.Optional[typing.Union[ConditionalAccessPolicyConditionsDevicesFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#filter ConditionalAccessPolicy#filter}
        '''
        value = ConditionalAccessPolicyConditionsDevices(filter=filter)

        return typing.cast(None, jsii.invoke(self, "putDevices", [value]))

    @jsii.member(jsii_name="putLocations")
    def put_locations(
        self,
        *,
        included_locations: typing.Sequence[builtins.str],
        excluded_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_locations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_locations ConditionalAccessPolicy#included_locations}.
        :param excluded_locations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_locations ConditionalAccessPolicy#excluded_locations}.
        '''
        value = ConditionalAccessPolicyConditionsLocations(
            included_locations=included_locations,
            excluded_locations=excluded_locations,
        )

        return typing.cast(None, jsii.invoke(self, "putLocations", [value]))

    @jsii.member(jsii_name="putPlatforms")
    def put_platforms(
        self,
        *,
        included_platforms: typing.Sequence[builtins.str],
        excluded_platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_platforms: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_platforms ConditionalAccessPolicy#included_platforms}.
        :param excluded_platforms: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_platforms ConditionalAccessPolicy#excluded_platforms}.
        '''
        value = ConditionalAccessPolicyConditionsPlatforms(
            included_platforms=included_platforms,
            excluded_platforms=excluded_platforms,
        )

        return typing.cast(None, jsii.invoke(self, "putPlatforms", [value]))

    @jsii.member(jsii_name="putUsers")
    def put_users(
        self,
        *,
        excluded_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_users: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excluded_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_groups ConditionalAccessPolicy#excluded_groups}.
        :param excluded_roles: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_roles ConditionalAccessPolicy#excluded_roles}.
        :param excluded_users: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_users ConditionalAccessPolicy#excluded_users}.
        :param included_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_groups ConditionalAccessPolicy#included_groups}.
        :param included_roles: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_roles ConditionalAccessPolicy#included_roles}.
        :param included_users: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_users ConditionalAccessPolicy#included_users}.
        '''
        value = ConditionalAccessPolicyConditionsUsers(
            excluded_groups=excluded_groups,
            excluded_roles=excluded_roles,
            excluded_users=excluded_users,
            included_groups=included_groups,
            included_roles=included_roles,
            included_users=included_users,
        )

        return typing.cast(None, jsii.invoke(self, "putUsers", [value]))

    @jsii.member(jsii_name="resetDevices")
    def reset_devices(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevices", []))

    @jsii.member(jsii_name="resetLocations")
    def reset_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocations", []))

    @jsii.member(jsii_name="resetPlatforms")
    def reset_platforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatforms", []))

    @jsii.member(jsii_name="resetSignInRiskLevels")
    def reset_sign_in_risk_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignInRiskLevels", []))

    @jsii.member(jsii_name="resetUserRiskLevels")
    def reset_user_risk_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserRiskLevels", []))

    @builtins.property
    @jsii.member(jsii_name="applications")
    def applications(
        self,
    ) -> ConditionalAccessPolicyConditionsApplicationsOutputReference:
        return typing.cast(ConditionalAccessPolicyConditionsApplicationsOutputReference, jsii.get(self, "applications"))

    @builtins.property
    @jsii.member(jsii_name="devices")
    def devices(self) -> ConditionalAccessPolicyConditionsDevicesOutputReference:
        return typing.cast(ConditionalAccessPolicyConditionsDevicesOutputReference, jsii.get(self, "devices"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> ConditionalAccessPolicyConditionsLocationsOutputReference:
        return typing.cast(ConditionalAccessPolicyConditionsLocationsOutputReference, jsii.get(self, "locations"))

    @builtins.property
    @jsii.member(jsii_name="platforms")
    def platforms(self) -> "ConditionalAccessPolicyConditionsPlatformsOutputReference":
        return typing.cast("ConditionalAccessPolicyConditionsPlatformsOutputReference", jsii.get(self, "platforms"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "ConditionalAccessPolicyConditionsUsersOutputReference":
        return typing.cast("ConditionalAccessPolicyConditionsUsersOutputReference", jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="applicationsInput")
    def applications_input(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsApplications]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsApplications], jsii.get(self, "applicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAppTypesInput")
    def client_app_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clientAppTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="devicesInput")
    def devices_input(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsDevices]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsDevices], jsii.get(self, "devicesInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsLocations]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsLocations], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="platformsInput")
    def platforms_input(
        self,
    ) -> typing.Optional["ConditionalAccessPolicyConditionsPlatforms"]:
        return typing.cast(typing.Optional["ConditionalAccessPolicyConditionsPlatforms"], jsii.get(self, "platformsInput"))

    @builtins.property
    @jsii.member(jsii_name="signInRiskLevelsInput")
    def sign_in_risk_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "signInRiskLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="userRiskLevelsInput")
    def user_risk_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userRiskLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(self) -> typing.Optional["ConditionalAccessPolicyConditionsUsers"]:
        return typing.cast(typing.Optional["ConditionalAccessPolicyConditionsUsers"], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAppTypes")
    def client_app_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clientAppTypes"))

    @client_app_types.setter
    def client_app_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5abab12356d461e8b348c8cf54a9a132444411540dcbfeac80a0bdfbdfe75c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAppTypes", value)

    @builtins.property
    @jsii.member(jsii_name="signInRiskLevels")
    def sign_in_risk_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "signInRiskLevels"))

    @sign_in_risk_levels.setter
    def sign_in_risk_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80700accaee621f14bcca575c1984dc9ca2f2ae798bd58905148dafe8837a63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signInRiskLevels", value)

    @builtins.property
    @jsii.member(jsii_name="userRiskLevels")
    def user_risk_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userRiskLevels"))

    @user_risk_levels.setter
    def user_risk_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84526cacbdf55c341f30ec6452e645434c2971cc9177be4e1235f7032c556e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userRiskLevels", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ConditionalAccessPolicyConditions]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicyConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3375036e27d7d9f847f9bc8c8827317024e825bfbda41a0df6059d7778fab9b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsPlatforms",
    jsii_struct_bases=[],
    name_mapping={
        "included_platforms": "includedPlatforms",
        "excluded_platforms": "excludedPlatforms",
    },
)
class ConditionalAccessPolicyConditionsPlatforms:
    def __init__(
        self,
        *,
        included_platforms: typing.Sequence[builtins.str],
        excluded_platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_platforms: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_platforms ConditionalAccessPolicy#included_platforms}.
        :param excluded_platforms: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_platforms ConditionalAccessPolicy#excluded_platforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7237d289833d8db0df836a3bdc399a5a484c0385a5dfa1ee7f01cb7fec59b3)
            check_type(argname="argument included_platforms", value=included_platforms, expected_type=type_hints["included_platforms"])
            check_type(argname="argument excluded_platforms", value=excluded_platforms, expected_type=type_hints["excluded_platforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "included_platforms": included_platforms,
        }
        if excluded_platforms is not None:
            self._values["excluded_platforms"] = excluded_platforms

    @builtins.property
    def included_platforms(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_platforms ConditionalAccessPolicy#included_platforms}.'''
        result = self._values.get("included_platforms")
        assert result is not None, "Required property 'included_platforms' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def excluded_platforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_platforms ConditionalAccessPolicy#excluded_platforms}.'''
        result = self._values.get("excluded_platforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyConditionsPlatforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalAccessPolicyConditionsPlatformsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsPlatformsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__257a02fa8972f1b1ff2d6a1222b992120c3d7dfc27160078666b572406fcfb8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedPlatforms")
    def reset_excluded_platforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedPlatforms", []))

    @builtins.property
    @jsii.member(jsii_name="excludedPlatformsInput")
    def excluded_platforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedPlatformsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedPlatformsInput")
    def included_platforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedPlatformsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedPlatforms")
    def excluded_platforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedPlatforms"))

    @excluded_platforms.setter
    def excluded_platforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3941a15b3bffb8643b648718c1e508041de429c17ebab4c9a4744eb403512838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedPlatforms", value)

    @builtins.property
    @jsii.member(jsii_name="includedPlatforms")
    def included_platforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedPlatforms"))

    @included_platforms.setter
    def included_platforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1abd70c1e6c3ff112d372676941516a277cae250dc38d59a3c554aacdc69588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedPlatforms", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConditionalAccessPolicyConditionsPlatforms]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsPlatforms], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicyConditionsPlatforms],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235c45a62861c0700e236d751c74c1e9c066b61a860df237aa168ba3af174f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsUsers",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_groups": "excludedGroups",
        "excluded_roles": "excludedRoles",
        "excluded_users": "excludedUsers",
        "included_groups": "includedGroups",
        "included_roles": "includedRoles",
        "included_users": "includedUsers",
    },
)
class ConditionalAccessPolicyConditionsUsers:
    def __init__(
        self,
        *,
        excluded_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_users: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excluded_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_groups ConditionalAccessPolicy#excluded_groups}.
        :param excluded_roles: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_roles ConditionalAccessPolicy#excluded_roles}.
        :param excluded_users: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_users ConditionalAccessPolicy#excluded_users}.
        :param included_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_groups ConditionalAccessPolicy#included_groups}.
        :param included_roles: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_roles ConditionalAccessPolicy#included_roles}.
        :param included_users: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_users ConditionalAccessPolicy#included_users}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d420b9f32eaa0075d74ecf3ef166a4e046a9362a27c48565bc339d975546884c)
            check_type(argname="argument excluded_groups", value=excluded_groups, expected_type=type_hints["excluded_groups"])
            check_type(argname="argument excluded_roles", value=excluded_roles, expected_type=type_hints["excluded_roles"])
            check_type(argname="argument excluded_users", value=excluded_users, expected_type=type_hints["excluded_users"])
            check_type(argname="argument included_groups", value=included_groups, expected_type=type_hints["included_groups"])
            check_type(argname="argument included_roles", value=included_roles, expected_type=type_hints["included_roles"])
            check_type(argname="argument included_users", value=included_users, expected_type=type_hints["included_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excluded_groups is not None:
            self._values["excluded_groups"] = excluded_groups
        if excluded_roles is not None:
            self._values["excluded_roles"] = excluded_roles
        if excluded_users is not None:
            self._values["excluded_users"] = excluded_users
        if included_groups is not None:
            self._values["included_groups"] = included_groups
        if included_roles is not None:
            self._values["included_roles"] = included_roles
        if included_users is not None:
            self._values["included_users"] = included_users

    @builtins.property
    def excluded_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_groups ConditionalAccessPolicy#excluded_groups}.'''
        result = self._values.get("excluded_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_roles ConditionalAccessPolicy#excluded_roles}.'''
        result = self._values.get("excluded_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#excluded_users ConditionalAccessPolicy#excluded_users}.'''
        result = self._values.get("excluded_users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_groups ConditionalAccessPolicy#included_groups}.'''
        result = self._values.get("included_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_roles ConditionalAccessPolicy#included_roles}.'''
        result = self._values.get("included_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#included_users ConditionalAccessPolicy#included_users}.'''
        result = self._values.get("included_users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyConditionsUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalAccessPolicyConditionsUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConditionsUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72402876876894096de68280bbe2fff536553a0befc629c56b08953b39c30a46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedGroups")
    def reset_excluded_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedGroups", []))

    @jsii.member(jsii_name="resetExcludedRoles")
    def reset_excluded_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedRoles", []))

    @jsii.member(jsii_name="resetExcludedUsers")
    def reset_excluded_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedUsers", []))

    @jsii.member(jsii_name="resetIncludedGroups")
    def reset_included_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedGroups", []))

    @jsii.member(jsii_name="resetIncludedRoles")
    def reset_included_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedRoles", []))

    @jsii.member(jsii_name="resetIncludedUsers")
    def reset_included_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedUsers", []))

    @builtins.property
    @jsii.member(jsii_name="excludedGroupsInput")
    def excluded_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedRolesInput")
    def excluded_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedUsersInput")
    def excluded_users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="includedGroupsInput")
    def included_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedRolesInput")
    def included_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedUsersInput")
    def included_users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedGroups")
    def excluded_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedGroups"))

    @excluded_groups.setter
    def excluded_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9388e7accf4f7279e89d33843ca7daf1ca0cb10ac6af13089490019a8dc858ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedGroups", value)

    @builtins.property
    @jsii.member(jsii_name="excludedRoles")
    def excluded_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedRoles"))

    @excluded_roles.setter
    def excluded_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940be16cb74ed6b38168079d5c5a57f64cacd057c3e5203d1c256922ad1ebdca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="excludedUsers")
    def excluded_users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedUsers"))

    @excluded_users.setter
    def excluded_users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414d289e881ab4ba7b0385d51e1aaa38fb6992673c8e1ed18847c6da6327cb8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedUsers", value)

    @builtins.property
    @jsii.member(jsii_name="includedGroups")
    def included_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedGroups"))

    @included_groups.setter
    def included_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7f0964acb3010cbde85cf634c5d011910a95d38ef041b58d5e60272a48e21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedGroups", value)

    @builtins.property
    @jsii.member(jsii_name="includedRoles")
    def included_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedRoles"))

    @included_roles.setter
    def included_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347123fffefc9bcf6f0f75f6edc55dac4310524d9d0e3d22cea4f4b822bc5f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="includedUsers")
    def included_users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedUsers"))

    @included_users.setter
    def included_users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38985a0cfa906b98880ad260099482d557e4a938d14c05807f953747d2300d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedUsers", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ConditionalAccessPolicyConditionsUsers]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyConditionsUsers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicyConditionsUsers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b295df4af58550834fa68de324b05dd88633db34f6f67fb323663a388af029b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "conditions": "conditions",
        "display_name": "displayName",
        "grant_controls": "grantControls",
        "state": "state",
        "id": "id",
        "session_controls": "sessionControls",
        "timeouts": "timeouts",
    },
)
class ConditionalAccessPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        conditions: typing.Union[ConditionalAccessPolicyConditions, typing.Dict[builtins.str, typing.Any]],
        display_name: builtins.str,
        grant_controls: typing.Union["ConditionalAccessPolicyGrantControls", typing.Dict[builtins.str, typing.Any]],
        state: builtins.str,
        id: typing.Optional[builtins.str] = None,
        session_controls: typing.Optional[typing.Union["ConditionalAccessPolicySessionControls", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ConditionalAccessPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#conditions ConditionalAccessPolicy#conditions}
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#display_name ConditionalAccessPolicy#display_name}.
        :param grant_controls: grant_controls block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#grant_controls ConditionalAccessPolicy#grant_controls}
        :param state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#state ConditionalAccessPolicy#state}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#id ConditionalAccessPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param session_controls: session_controls block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#session_controls ConditionalAccessPolicy#session_controls}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#timeouts ConditionalAccessPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(conditions, dict):
            conditions = ConditionalAccessPolicyConditions(**conditions)
        if isinstance(grant_controls, dict):
            grant_controls = ConditionalAccessPolicyGrantControls(**grant_controls)
        if isinstance(session_controls, dict):
            session_controls = ConditionalAccessPolicySessionControls(**session_controls)
        if isinstance(timeouts, dict):
            timeouts = ConditionalAccessPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5419733fd88d6a1a7742547ff691727e492b0d3d4d4dbae1a5724b01d6a70d86)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument grant_controls", value=grant_controls, expected_type=type_hints["grant_controls"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument session_controls", value=session_controls, expected_type=type_hints["session_controls"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conditions": conditions,
            "display_name": display_name,
            "grant_controls": grant_controls,
            "state": state,
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
        if id is not None:
            self._values["id"] = id
        if session_controls is not None:
            self._values["session_controls"] = session_controls
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
    def conditions(self) -> ConditionalAccessPolicyConditions:
        '''conditions block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#conditions ConditionalAccessPolicy#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(ConditionalAccessPolicyConditions, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#display_name ConditionalAccessPolicy#display_name}.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grant_controls(self) -> "ConditionalAccessPolicyGrantControls":
        '''grant_controls block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#grant_controls ConditionalAccessPolicy#grant_controls}
        '''
        result = self._values.get("grant_controls")
        assert result is not None, "Required property 'grant_controls' is missing"
        return typing.cast("ConditionalAccessPolicyGrantControls", result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#state ConditionalAccessPolicy#state}.'''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#id ConditionalAccessPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_controls(
        self,
    ) -> typing.Optional["ConditionalAccessPolicySessionControls"]:
        '''session_controls block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#session_controls ConditionalAccessPolicy#session_controls}
        '''
        result = self._values.get("session_controls")
        return typing.cast(typing.Optional["ConditionalAccessPolicySessionControls"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ConditionalAccessPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#timeouts ConditionalAccessPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ConditionalAccessPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyGrantControls",
    jsii_struct_bases=[],
    name_mapping={
        "built_in_controls": "builtInControls",
        "operator": "operator",
        "custom_authentication_factors": "customAuthenticationFactors",
        "terms_of_use": "termsOfUse",
    },
)
class ConditionalAccessPolicyGrantControls:
    def __init__(
        self,
        *,
        built_in_controls: typing.Sequence[builtins.str],
        operator: builtins.str,
        custom_authentication_factors: typing.Optional[typing.Sequence[builtins.str]] = None,
        terms_of_use: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param built_in_controls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#built_in_controls ConditionalAccessPolicy#built_in_controls}.
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#operator ConditionalAccessPolicy#operator}.
        :param custom_authentication_factors: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#custom_authentication_factors ConditionalAccessPolicy#custom_authentication_factors}.
        :param terms_of_use: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#terms_of_use ConditionalAccessPolicy#terms_of_use}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e9ef9bc2dc88dde4df59064989633b969d7e38d3c80705e18758f2a3d80ff9)
            check_type(argname="argument built_in_controls", value=built_in_controls, expected_type=type_hints["built_in_controls"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument custom_authentication_factors", value=custom_authentication_factors, expected_type=type_hints["custom_authentication_factors"])
            check_type(argname="argument terms_of_use", value=terms_of_use, expected_type=type_hints["terms_of_use"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "built_in_controls": built_in_controls,
            "operator": operator,
        }
        if custom_authentication_factors is not None:
            self._values["custom_authentication_factors"] = custom_authentication_factors
        if terms_of_use is not None:
            self._values["terms_of_use"] = terms_of_use

    @builtins.property
    def built_in_controls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#built_in_controls ConditionalAccessPolicy#built_in_controls}.'''
        result = self._values.get("built_in_controls")
        assert result is not None, "Required property 'built_in_controls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#operator ConditionalAccessPolicy#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_authentication_factors(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#custom_authentication_factors ConditionalAccessPolicy#custom_authentication_factors}.'''
        result = self._values.get("custom_authentication_factors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def terms_of_use(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#terms_of_use ConditionalAccessPolicy#terms_of_use}.'''
        result = self._values.get("terms_of_use")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyGrantControls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalAccessPolicyGrantControlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyGrantControlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e65c680901dc948faa1c6303a18e5296ed2a0ab0ede671283235b27e19b9f56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomAuthenticationFactors")
    def reset_custom_authentication_factors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAuthenticationFactors", []))

    @jsii.member(jsii_name="resetTermsOfUse")
    def reset_terms_of_use(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTermsOfUse", []))

    @builtins.property
    @jsii.member(jsii_name="builtInControlsInput")
    def built_in_controls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "builtInControlsInput"))

    @builtins.property
    @jsii.member(jsii_name="customAuthenticationFactorsInput")
    def custom_authentication_factors_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customAuthenticationFactorsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="termsOfUseInput")
    def terms_of_use_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "termsOfUseInput"))

    @builtins.property
    @jsii.member(jsii_name="builtInControls")
    def built_in_controls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "builtInControls"))

    @built_in_controls.setter
    def built_in_controls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106aa2bae5c9136d7b817c1a6f06e039653a648bb56e37e9c41d0eb72071c6d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "builtInControls", value)

    @builtins.property
    @jsii.member(jsii_name="customAuthenticationFactors")
    def custom_authentication_factors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customAuthenticationFactors"))

    @custom_authentication_factors.setter
    def custom_authentication_factors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feec6b8bd3a02bb338872f90bbee17f1f1907f069463e9469bf1502e5dc835a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAuthenticationFactors", value)

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0845a509074e99b2fe56ec5e9726d7878b98afc087c7ffac778b9ba79975e028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="termsOfUse")
    def terms_of_use(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "termsOfUse"))

    @terms_of_use.setter
    def terms_of_use(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999a0a1127b347b6ba18218d4d85c97b1de5a692334e03a33e5453fd008910f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "termsOfUse", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ConditionalAccessPolicyGrantControls]:
        return typing.cast(typing.Optional[ConditionalAccessPolicyGrantControls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicyGrantControls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d717bdfe7f3db045ad237a475db2576444c5ceda596f4692e90f3c50a427385a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicySessionControls",
    jsii_struct_bases=[],
    name_mapping={
        "application_enforced_restrictions_enabled": "applicationEnforcedRestrictionsEnabled",
        "cloud_app_security_policy": "cloudAppSecurityPolicy",
        "persistent_browser_mode": "persistentBrowserMode",
        "sign_in_frequency": "signInFrequency",
        "sign_in_frequency_period": "signInFrequencyPeriod",
    },
)
class ConditionalAccessPolicySessionControls:
    def __init__(
        self,
        *,
        application_enforced_restrictions_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cloud_app_security_policy: typing.Optional[builtins.str] = None,
        persistent_browser_mode: typing.Optional[builtins.str] = None,
        sign_in_frequency: typing.Optional[jsii.Number] = None,
        sign_in_frequency_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_enforced_restrictions_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#application_enforced_restrictions_enabled ConditionalAccessPolicy#application_enforced_restrictions_enabled}.
        :param cloud_app_security_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#cloud_app_security_policy ConditionalAccessPolicy#cloud_app_security_policy}.
        :param persistent_browser_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#persistent_browser_mode ConditionalAccessPolicy#persistent_browser_mode}.
        :param sign_in_frequency: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_frequency ConditionalAccessPolicy#sign_in_frequency}.
        :param sign_in_frequency_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_frequency_period ConditionalAccessPolicy#sign_in_frequency_period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c236e180b6f7b64c571e9f407daabca05f3cd6329842ee7ae4bf5180bc8dbd67)
            check_type(argname="argument application_enforced_restrictions_enabled", value=application_enforced_restrictions_enabled, expected_type=type_hints["application_enforced_restrictions_enabled"])
            check_type(argname="argument cloud_app_security_policy", value=cloud_app_security_policy, expected_type=type_hints["cloud_app_security_policy"])
            check_type(argname="argument persistent_browser_mode", value=persistent_browser_mode, expected_type=type_hints["persistent_browser_mode"])
            check_type(argname="argument sign_in_frequency", value=sign_in_frequency, expected_type=type_hints["sign_in_frequency"])
            check_type(argname="argument sign_in_frequency_period", value=sign_in_frequency_period, expected_type=type_hints["sign_in_frequency_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_enforced_restrictions_enabled is not None:
            self._values["application_enforced_restrictions_enabled"] = application_enforced_restrictions_enabled
        if cloud_app_security_policy is not None:
            self._values["cloud_app_security_policy"] = cloud_app_security_policy
        if persistent_browser_mode is not None:
            self._values["persistent_browser_mode"] = persistent_browser_mode
        if sign_in_frequency is not None:
            self._values["sign_in_frequency"] = sign_in_frequency
        if sign_in_frequency_period is not None:
            self._values["sign_in_frequency_period"] = sign_in_frequency_period

    @builtins.property
    def application_enforced_restrictions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#application_enforced_restrictions_enabled ConditionalAccessPolicy#application_enforced_restrictions_enabled}.'''
        result = self._values.get("application_enforced_restrictions_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cloud_app_security_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#cloud_app_security_policy ConditionalAccessPolicy#cloud_app_security_policy}.'''
        result = self._values.get("cloud_app_security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistent_browser_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#persistent_browser_mode ConditionalAccessPolicy#persistent_browser_mode}.'''
        result = self._values.get("persistent_browser_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_in_frequency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_frequency ConditionalAccessPolicy#sign_in_frequency}.'''
        result = self._values.get("sign_in_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sign_in_frequency_period(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#sign_in_frequency_period ConditionalAccessPolicy#sign_in_frequency_period}.'''
        result = self._values.get("sign_in_frequency_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicySessionControls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalAccessPolicySessionControlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicySessionControlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b4b40152a165e3388600c952bdd60ebfc72bc09b22f31b7c17fb9a3974d274)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApplicationEnforcedRestrictionsEnabled")
    def reset_application_enforced_restrictions_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationEnforcedRestrictionsEnabled", []))

    @jsii.member(jsii_name="resetCloudAppSecurityPolicy")
    def reset_cloud_app_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudAppSecurityPolicy", []))

    @jsii.member(jsii_name="resetPersistentBrowserMode")
    def reset_persistent_browser_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistentBrowserMode", []))

    @jsii.member(jsii_name="resetSignInFrequency")
    def reset_sign_in_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignInFrequency", []))

    @jsii.member(jsii_name="resetSignInFrequencyPeriod")
    def reset_sign_in_frequency_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignInFrequencyPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="applicationEnforcedRestrictionsEnabledInput")
    def application_enforced_restrictions_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "applicationEnforcedRestrictionsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudAppSecurityPolicyInput")
    def cloud_app_security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudAppSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="persistentBrowserModeInput")
    def persistent_browser_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "persistentBrowserModeInput"))

    @builtins.property
    @jsii.member(jsii_name="signInFrequencyInput")
    def sign_in_frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "signInFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="signInFrequencyPeriodInput")
    def sign_in_frequency_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signInFrequencyPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationEnforcedRestrictionsEnabled")
    def application_enforced_restrictions_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "applicationEnforcedRestrictionsEnabled"))

    @application_enforced_restrictions_enabled.setter
    def application_enforced_restrictions_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956b59b8c26f67d4b460f59e21c45429e390134cbf86eb5fed15febc57b640cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationEnforcedRestrictionsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cloudAppSecurityPolicy")
    def cloud_app_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudAppSecurityPolicy"))

    @cloud_app_security_policy.setter
    def cloud_app_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e23146cd60b7a090f0b41e3b0aee7c058f3eaa7ee2f49f50dfd16111a782ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudAppSecurityPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="persistentBrowserMode")
    def persistent_browser_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "persistentBrowserMode"))

    @persistent_browser_mode.setter
    def persistent_browser_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033ceaacd84f5f0a89397ddf4f18263a9679070f613a3af1d8b64077d0699ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "persistentBrowserMode", value)

    @builtins.property
    @jsii.member(jsii_name="signInFrequency")
    def sign_in_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "signInFrequency"))

    @sign_in_frequency.setter
    def sign_in_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0099fcd0c9b43fad8f8d3b0a6ddea312a9fc2879e095c6e316b34954bdc705a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signInFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="signInFrequencyPeriod")
    def sign_in_frequency_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signInFrequencyPeriod"))

    @sign_in_frequency_period.setter
    def sign_in_frequency_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2d3327d68a8ea1a8b955808f24546f6f4dd138fb0d43be6ba722d7388ffd67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signInFrequencyPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ConditionalAccessPolicySessionControls]:
        return typing.cast(typing.Optional[ConditionalAccessPolicySessionControls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConditionalAccessPolicySessionControls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6beb3436dbe016930e0c1d7883f71c0fbcff50a4ff77d0ae50700ccd5907473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ConditionalAccessPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#create ConditionalAccessPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#delete ConditionalAccessPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#read ConditionalAccessPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#update ConditionalAccessPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255d99d58932dd4166afce796241f18cd1e78a2ac28a6d791221834afc790d42)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#create ConditionalAccessPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#delete ConditionalAccessPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#read ConditionalAccessPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azuread/r/conditional_access_policy#update ConditionalAccessPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalAccessPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalAccessPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.conditionalAccessPolicy.ConditionalAccessPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3738857f8c774bf692bfa9642675c54b608273f0fed977c506538620118baa7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a17b0e9a2a2728db9db14861e242390f2c5dcc1d660c976f05493776aae917b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336791233e3229958838f139d94c0a5a824c2811b7de2b21fb66a230c605e1ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1ee4be25d616372915fc07f20b0401af92a475f4d5997876a722e220fd7134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9cc765899dd7c933a864102f68eed6c55efdffc45caad4da1f5a3736a4bbcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ConditionalAccessPolicyTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ConditionalAccessPolicyTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ConditionalAccessPolicyTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fd82dae1ae613ad37f71c289504dcc18a86b5e5007d79ef1b144f0582487bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ConditionalAccessPolicy",
    "ConditionalAccessPolicyConditions",
    "ConditionalAccessPolicyConditionsApplications",
    "ConditionalAccessPolicyConditionsApplicationsOutputReference",
    "ConditionalAccessPolicyConditionsDevices",
    "ConditionalAccessPolicyConditionsDevicesFilter",
    "ConditionalAccessPolicyConditionsDevicesFilterOutputReference",
    "ConditionalAccessPolicyConditionsDevicesOutputReference",
    "ConditionalAccessPolicyConditionsLocations",
    "ConditionalAccessPolicyConditionsLocationsOutputReference",
    "ConditionalAccessPolicyConditionsOutputReference",
    "ConditionalAccessPolicyConditionsPlatforms",
    "ConditionalAccessPolicyConditionsPlatformsOutputReference",
    "ConditionalAccessPolicyConditionsUsers",
    "ConditionalAccessPolicyConditionsUsersOutputReference",
    "ConditionalAccessPolicyConfig",
    "ConditionalAccessPolicyGrantControls",
    "ConditionalAccessPolicyGrantControlsOutputReference",
    "ConditionalAccessPolicySessionControls",
    "ConditionalAccessPolicySessionControlsOutputReference",
    "ConditionalAccessPolicyTimeouts",
    "ConditionalAccessPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bda8e7441b6c17a94a8f11203cb1e09fdd85e21778b3a7504886befd5467b549(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    conditions: typing.Union[ConditionalAccessPolicyConditions, typing.Dict[builtins.str, typing.Any]],
    display_name: builtins.str,
    grant_controls: typing.Union[ConditionalAccessPolicyGrantControls, typing.Dict[builtins.str, typing.Any]],
    state: builtins.str,
    id: typing.Optional[builtins.str] = None,
    session_controls: typing.Optional[typing.Union[ConditionalAccessPolicySessionControls, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ConditionalAccessPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0d18a0404f165bfdb4ea8c14882156509c53466357b61d759c2143265947f45c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342ac25be951f7194888f7ba4e2320e9df9c00d0cb3abe1617379409f9d2c951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90be1c5002ea4b6b68e2c267c3c472c2dc471b8a056dfe9c31891d1c80d536fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6ca498f70a8dfc5ca12bb3ca3b60ed0decb89bca1f16d3eb3835416a5c6355(
    *,
    applications: typing.Union[ConditionalAccessPolicyConditionsApplications, typing.Dict[builtins.str, typing.Any]],
    client_app_types: typing.Sequence[builtins.str],
    users: typing.Union[ConditionalAccessPolicyConditionsUsers, typing.Dict[builtins.str, typing.Any]],
    devices: typing.Optional[typing.Union[ConditionalAccessPolicyConditionsDevices, typing.Dict[builtins.str, typing.Any]]] = None,
    locations: typing.Optional[typing.Union[ConditionalAccessPolicyConditionsLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    platforms: typing.Optional[typing.Union[ConditionalAccessPolicyConditionsPlatforms, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_in_risk_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_risk_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11026c77806c5638ff31deed764671983442729eab6de259f981e4c908541f3d(
    *,
    excluded_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_user_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a676bd53c40d07330145257c71816fe95b1d855afa31f76b0863a0a2792019(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ab46b5507641840d8949499b472c6c92ed035112342750e5c4889d634d7f00(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e839be7313e78c97bf4138370ee51df87bb1341610ccd0e80322fc16437e3a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a4e85ea0367fc0583aa794febc9e3cde4c69679e8d175d19539454f376f34a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d941fe07358af071bdf274dda21da709cf19acea868060a88b5e138936d784a5(
    value: typing.Optional[ConditionalAccessPolicyConditionsApplications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10c350974ac5d12ae2af28f283d7438255f38b9521f79e8b6f4eced175ce5cf(
    *,
    filter: typing.Optional[typing.Union[ConditionalAccessPolicyConditionsDevicesFilter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ef6a53b1c5c09838967f0d12f8571d12ff78e2108dfcac619ea0b0cd24911b(
    *,
    mode: builtins.str,
    rule: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecb07c2222332c25d550601fd14f2c0dca72cd0070180f4dbac9e643e41218b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebad9b002ea036162bbadde106cb69e4570429b663c426366e849ca6e9455ff4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37d0569adba8fbef8f8f465fb188a4d5e698f89903589abbf79f6a55850810b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3977248f725b9010cef3cc316c56c9467452bc0efdb66cf9daa757267a73563(
    value: typing.Optional[ConditionalAccessPolicyConditionsDevicesFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe3b86180f822c41519d6f4bb6370130051e114607799ae0c5cde1044c00c7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1829bc397b7f24258976851673507c9eb6333f185381c2e2c6b61eab3aeff732(
    value: typing.Optional[ConditionalAccessPolicyConditionsDevices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c7305eb364afef5b292e50c63c9b45344be7eb5e3a26e450df5391eb9c959e(
    *,
    included_locations: typing.Sequence[builtins.str],
    excluded_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfa937160d76f86e7e6d239a2e3bae1ac2edafbe66b41da9cb51a4dfdc17fdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a8fc9de65b1c675b9903c72212e0af17a6a6652fb88606f9f42697cb35f3b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64dfcd9642f63298175cef996acc07af6e466cf67a219b06cf4f5200ca700e39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11347f7b2296191f5aefe02b8031b7e47a87bd5da8a12937bff31101a6a78d78(
    value: typing.Optional[ConditionalAccessPolicyConditionsLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8d93a80edffae6b02ed055a4fa9d61f3439be406e051d81fc0b1f62464e1f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5abab12356d461e8b348c8cf54a9a132444411540dcbfeac80a0bdfbdfe75c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80700accaee621f14bcca575c1984dc9ca2f2ae798bd58905148dafe8837a63c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84526cacbdf55c341f30ec6452e645434c2971cc9177be4e1235f7032c556e91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3375036e27d7d9f847f9bc8c8827317024e825bfbda41a0df6059d7778fab9b3(
    value: typing.Optional[ConditionalAccessPolicyConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7237d289833d8db0df836a3bdc399a5a484c0385a5dfa1ee7f01cb7fec59b3(
    *,
    included_platforms: typing.Sequence[builtins.str],
    excluded_platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257a02fa8972f1b1ff2d6a1222b992120c3d7dfc27160078666b572406fcfb8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3941a15b3bffb8643b648718c1e508041de429c17ebab4c9a4744eb403512838(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1abd70c1e6c3ff112d372676941516a277cae250dc38d59a3c554aacdc69588(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235c45a62861c0700e236d751c74c1e9c066b61a860df237aa168ba3af174f19(
    value: typing.Optional[ConditionalAccessPolicyConditionsPlatforms],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d420b9f32eaa0075d74ecf3ef166a4e046a9362a27c48565bc339d975546884c(
    *,
    excluded_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72402876876894096de68280bbe2fff536553a0befc629c56b08953b39c30a46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9388e7accf4f7279e89d33843ca7daf1ca0cb10ac6af13089490019a8dc858ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940be16cb74ed6b38168079d5c5a57f64cacd057c3e5203d1c256922ad1ebdca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414d289e881ab4ba7b0385d51e1aaa38fb6992673c8e1ed18847c6da6327cb8e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7f0964acb3010cbde85cf634c5d011910a95d38ef041b58d5e60272a48e21f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347123fffefc9bcf6f0f75f6edc55dac4310524d9d0e3d22cea4f4b822bc5f27(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38985a0cfa906b98880ad260099482d557e4a938d14c05807f953747d2300d93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b295df4af58550834fa68de324b05dd88633db34f6f67fb323663a388af029b(
    value: typing.Optional[ConditionalAccessPolicyConditionsUsers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5419733fd88d6a1a7742547ff691727e492b0d3d4d4dbae1a5724b01d6a70d86(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    conditions: typing.Union[ConditionalAccessPolicyConditions, typing.Dict[builtins.str, typing.Any]],
    display_name: builtins.str,
    grant_controls: typing.Union[ConditionalAccessPolicyGrantControls, typing.Dict[builtins.str, typing.Any]],
    state: builtins.str,
    id: typing.Optional[builtins.str] = None,
    session_controls: typing.Optional[typing.Union[ConditionalAccessPolicySessionControls, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ConditionalAccessPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e9ef9bc2dc88dde4df59064989633b969d7e38d3c80705e18758f2a3d80ff9(
    *,
    built_in_controls: typing.Sequence[builtins.str],
    operator: builtins.str,
    custom_authentication_factors: typing.Optional[typing.Sequence[builtins.str]] = None,
    terms_of_use: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e65c680901dc948faa1c6303a18e5296ed2a0ab0ede671283235b27e19b9f56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106aa2bae5c9136d7b817c1a6f06e039653a648bb56e37e9c41d0eb72071c6d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feec6b8bd3a02bb338872f90bbee17f1f1907f069463e9469bf1502e5dc835a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0845a509074e99b2fe56ec5e9726d7878b98afc087c7ffac778b9ba79975e028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999a0a1127b347b6ba18218d4d85c97b1de5a692334e03a33e5453fd008910f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d717bdfe7f3db045ad237a475db2576444c5ceda596f4692e90f3c50a427385a(
    value: typing.Optional[ConditionalAccessPolicyGrantControls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c236e180b6f7b64c571e9f407daabca05f3cd6329842ee7ae4bf5180bc8dbd67(
    *,
    application_enforced_restrictions_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cloud_app_security_policy: typing.Optional[builtins.str] = None,
    persistent_browser_mode: typing.Optional[builtins.str] = None,
    sign_in_frequency: typing.Optional[jsii.Number] = None,
    sign_in_frequency_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b4b40152a165e3388600c952bdd60ebfc72bc09b22f31b7c17fb9a3974d274(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956b59b8c26f67d4b460f59e21c45429e390134cbf86eb5fed15febc57b640cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e23146cd60b7a090f0b41e3b0aee7c058f3eaa7ee2f49f50dfd16111a782ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033ceaacd84f5f0a89397ddf4f18263a9679070f613a3af1d8b64077d0699ad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0099fcd0c9b43fad8f8d3b0a6ddea312a9fc2879e095c6e316b34954bdc705a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2d3327d68a8ea1a8b955808f24546f6f4dd138fb0d43be6ba722d7388ffd67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6beb3436dbe016930e0c1d7883f71c0fbcff50a4ff77d0ae50700ccd5907473(
    value: typing.Optional[ConditionalAccessPolicySessionControls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255d99d58932dd4166afce796241f18cd1e78a2ac28a6d791221834afc790d42(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3738857f8c774bf692bfa9642675c54b608273f0fed977c506538620118baa7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17b0e9a2a2728db9db14861e242390f2c5dcc1d660c976f05493776aae917b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336791233e3229958838f139d94c0a5a824c2811b7de2b21fb66a230c605e1ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1ee4be25d616372915fc07f20b0401af92a475f4d5997876a722e220fd7134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9cc765899dd7c933a864102f68eed6c55efdffc45caad4da1f5a3736a4bbcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fd82dae1ae613ad37f71c289504dcc18a86b5e5007d79ef1b144f0582487bc(
    value: typing.Optional[typing.Union[ConditionalAccessPolicyTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
