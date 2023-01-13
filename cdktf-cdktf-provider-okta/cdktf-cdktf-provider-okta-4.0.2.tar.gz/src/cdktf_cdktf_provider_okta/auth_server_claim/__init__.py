'''
# `okta_auth_server_claim`

Refer to the Terraform Registory for docs: [`okta_auth_server_claim`](https://www.terraform.io/docs/providers/okta/r/auth_server_claim).
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


class AuthServerClaim(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.authServerClaim.AuthServerClaim",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim okta_auth_server_claim}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auth_server_id: builtins.str,
        claim_type: builtins.str,
        name: builtins.str,
        value: builtins.str,
        always_include_in_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_filter_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        value_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim okta_auth_server_claim} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_server_id: Auth server ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#auth_server_id AuthServerClaim#auth_server_id}
        :param claim_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#claim_type AuthServerClaim#claim_type}.
        :param name: Auth server claim name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#name AuthServerClaim#name}
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#value AuthServerClaim#value}.
        :param always_include_in_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#always_include_in_token AuthServerClaim#always_include_in_token}.
        :param group_filter_type: Required when value_type is GROUPS. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#group_filter_type AuthServerClaim#group_filter_type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#id AuthServerClaim#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scopes: Auth server claim list of scopes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#scopes AuthServerClaim#scopes}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#status AuthServerClaim#status}.
        :param value_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#value_type AuthServerClaim#value_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb33a3a75d385024de4ddaa5937884caa519b1a776d3a0330e869a248e4cc7c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AuthServerClaimConfig(
            auth_server_id=auth_server_id,
            claim_type=claim_type,
            name=name,
            value=value,
            always_include_in_token=always_include_in_token,
            group_filter_type=group_filter_type,
            id=id,
            scopes=scopes,
            status=status,
            value_type=value_type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAlwaysIncludeInToken")
    def reset_always_include_in_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysIncludeInToken", []))

    @jsii.member(jsii_name="resetGroupFilterType")
    def reset_group_filter_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupFilterType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetValueType")
    def reset_value_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="alwaysIncludeInTokenInput")
    def always_include_in_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alwaysIncludeInTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="authServerIdInput")
    def auth_server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authServerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="claimTypeInput")
    def claim_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "claimTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupFilterTypeInput")
    def group_filter_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupFilterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="valueTypeInput")
    def value_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysIncludeInToken")
    def always_include_in_token(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alwaysIncludeInToken"))

    @always_include_in_token.setter
    def always_include_in_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8fe4c5081941f5f61d1f4e7fb9c2b2c17d1886c22761187bd0115d63ca6098f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysIncludeInToken", value)

    @builtins.property
    @jsii.member(jsii_name="authServerId")
    def auth_server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authServerId"))

    @auth_server_id.setter
    def auth_server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b607455082c28bfaa506840c8b6f9c439b4c9431cadea6459757a995e53c579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authServerId", value)

    @builtins.property
    @jsii.member(jsii_name="claimType")
    def claim_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "claimType"))

    @claim_type.setter
    def claim_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53f986699a407eb33a89d4a9d4826b1f427784e3f9ed120b7a9913bb62bba46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "claimType", value)

    @builtins.property
    @jsii.member(jsii_name="groupFilterType")
    def group_filter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupFilterType"))

    @group_filter_type.setter
    def group_filter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b0fc2b99735aeeb34f02806948936617a67910b455b2fc71eed44a5ac42938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupFilterType", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8e02677f619e6bfcefcf015f662e5bfaab3edfa1366959f0464af67f9abddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588880a7c7d790df03f03d7c8992590ed360525aedad4f5d1cd8d477c96d159d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70565f0b59f5a993ec427391e42f91b9e5a95b1b4db1c1b83997eb4790c5227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1640903c3001f5f0fb3449fbcc6962fa35c064f68e17e3c207a68ec7db531d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72279ab2d2c27e864a4eec9888eeb46bd5529e2f6000cbf4220e04bf1cb916d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed55d1aa648a698d668994a90726ce0761aae0198e462668238923916b27ac6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.authServerClaim.AuthServerClaimConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auth_server_id": "authServerId",
        "claim_type": "claimType",
        "name": "name",
        "value": "value",
        "always_include_in_token": "alwaysIncludeInToken",
        "group_filter_type": "groupFilterType",
        "id": "id",
        "scopes": "scopes",
        "status": "status",
        "value_type": "valueType",
    },
)
class AuthServerClaimConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auth_server_id: builtins.str,
        claim_type: builtins.str,
        name: builtins.str,
        value: builtins.str,
        always_include_in_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_filter_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        value_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auth_server_id: Auth server ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#auth_server_id AuthServerClaim#auth_server_id}
        :param claim_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#claim_type AuthServerClaim#claim_type}.
        :param name: Auth server claim name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#name AuthServerClaim#name}
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#value AuthServerClaim#value}.
        :param always_include_in_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#always_include_in_token AuthServerClaim#always_include_in_token}.
        :param group_filter_type: Required when value_type is GROUPS. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#group_filter_type AuthServerClaim#group_filter_type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#id AuthServerClaim#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scopes: Auth server claim list of scopes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#scopes AuthServerClaim#scopes}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#status AuthServerClaim#status}.
        :param value_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#value_type AuthServerClaim#value_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f318e9001cfc402e37a4ec789d1c5b38a8173454c88c6c76131ee536855f345)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auth_server_id", value=auth_server_id, expected_type=type_hints["auth_server_id"])
            check_type(argname="argument claim_type", value=claim_type, expected_type=type_hints["claim_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument always_include_in_token", value=always_include_in_token, expected_type=type_hints["always_include_in_token"])
            check_type(argname="argument group_filter_type", value=group_filter_type, expected_type=type_hints["group_filter_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_server_id": auth_server_id,
            "claim_type": claim_type,
            "name": name,
            "value": value,
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
        if always_include_in_token is not None:
            self._values["always_include_in_token"] = always_include_in_token
        if group_filter_type is not None:
            self._values["group_filter_type"] = group_filter_type
        if id is not None:
            self._values["id"] = id
        if scopes is not None:
            self._values["scopes"] = scopes
        if status is not None:
            self._values["status"] = status
        if value_type is not None:
            self._values["value_type"] = value_type

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
    def auth_server_id(self) -> builtins.str:
        '''Auth server ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#auth_server_id AuthServerClaim#auth_server_id}
        '''
        result = self._values.get("auth_server_id")
        assert result is not None, "Required property 'auth_server_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def claim_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#claim_type AuthServerClaim#claim_type}.'''
        result = self._values.get("claim_type")
        assert result is not None, "Required property 'claim_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Auth server claim name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#name AuthServerClaim#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#value AuthServerClaim#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_include_in_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#always_include_in_token AuthServerClaim#always_include_in_token}.'''
        result = self._values.get("always_include_in_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_filter_type(self) -> typing.Optional[builtins.str]:
        '''Required when value_type is GROUPS.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#group_filter_type AuthServerClaim#group_filter_type}
        '''
        result = self._values.get("group_filter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#id AuthServerClaim#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Auth server claim list of scopes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#scopes AuthServerClaim#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#status AuthServerClaim#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_claim#value_type AuthServerClaim#value_type}.'''
        result = self._values.get("value_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthServerClaimConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AuthServerClaim",
    "AuthServerClaimConfig",
]

publication.publish()

def _typecheckingstub__7eb33a3a75d385024de4ddaa5937884caa519b1a776d3a0330e869a248e4cc7c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auth_server_id: builtins.str,
    claim_type: builtins.str,
    name: builtins.str,
    value: builtins.str,
    always_include_in_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_filter_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    value_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a8fe4c5081941f5f61d1f4e7fb9c2b2c17d1886c22761187bd0115d63ca6098f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b607455082c28bfaa506840c8b6f9c439b4c9431cadea6459757a995e53c579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53f986699a407eb33a89d4a9d4826b1f427784e3f9ed120b7a9913bb62bba46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b0fc2b99735aeeb34f02806948936617a67910b455b2fc71eed44a5ac42938(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8e02677f619e6bfcefcf015f662e5bfaab3edfa1366959f0464af67f9abddd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588880a7c7d790df03f03d7c8992590ed360525aedad4f5d1cd8d477c96d159d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70565f0b59f5a993ec427391e42f91b9e5a95b1b4db1c1b83997eb4790c5227(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1640903c3001f5f0fb3449fbcc6962fa35c064f68e17e3c207a68ec7db531d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72279ab2d2c27e864a4eec9888eeb46bd5529e2f6000cbf4220e04bf1cb916d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed55d1aa648a698d668994a90726ce0761aae0198e462668238923916b27ac6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f318e9001cfc402e37a4ec789d1c5b38a8173454c88c6c76131ee536855f345(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_server_id: builtins.str,
    claim_type: builtins.str,
    name: builtins.str,
    value: builtins.str,
    always_include_in_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_filter_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
