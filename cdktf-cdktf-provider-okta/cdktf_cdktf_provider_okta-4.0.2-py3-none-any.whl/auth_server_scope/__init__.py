'''
# `okta_auth_server_scope`

Refer to the Terraform Registory for docs: [`okta_auth_server_scope`](https://www.terraform.io/docs/providers/okta/r/auth_server_scope).
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


class AuthServerScope(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.authServerScope.AuthServerScope",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope okta_auth_server_scope}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auth_server_id: builtins.str,
        name: builtins.str,
        consent: typing.Optional[builtins.str] = None,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata_publish: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope okta_auth_server_scope} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_server_id: Auth server ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#auth_server_id AuthServerScope#auth_server_id}
        :param name: Auth server scope name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#name AuthServerScope#name}
        :param consent: EA Feature and thus it is simply ignored if the feature is off. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#consent AuthServerScope#consent}
        :param default: A default scope will be returned in an access token when the client omits the scope parameter in a token request, provided this scope is allowed as part of the access policy rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#default AuthServerScope#default}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#description AuthServerScope#description}.
        :param display_name: Name of the end user displayed in a consent dialog box. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#display_name AuthServerScope#display_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#id AuthServerScope#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata_publish: Whether to publish metadata or not, matching API type despite the fact it could just be a boolean. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#metadata_publish AuthServerScope#metadata_publish}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25e7b90d2ad183108cc9094b2acf1910236937c2a20d4ea539b047677e02683)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AuthServerScopeConfig(
            auth_server_id=auth_server_id,
            name=name,
            consent=consent,
            default=default,
            description=description,
            display_name=display_name,
            id=id,
            metadata_publish=metadata_publish,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetConsent")
    def reset_consent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsent", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetadataPublish")
    def reset_metadata_publish(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataPublish", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="systemAttribute")
    def system_attribute(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "systemAttribute"))

    @builtins.property
    @jsii.member(jsii_name="authServerIdInput")
    def auth_server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authServerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consentInput")
    def consent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consentInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataPublishInput")
    def metadata_publish_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataPublishInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="authServerId")
    def auth_server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authServerId"))

    @auth_server_id.setter
    def auth_server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e3ad33ccab21ed3da6b69604cf36301cbd1a82bdeebae3403a7db722cf97fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authServerId", value)

    @builtins.property
    @jsii.member(jsii_name="consent")
    def consent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consent"))

    @consent.setter
    def consent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e505fb5d0049e482cedcf5bc3a19b10f03683a4f6e73faeff5b3902e78fd14b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consent", value)

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed708b172240fed145d48a3d5c4fe753988e75899a705e3f329809a2721762b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b49982b35a51b969913b1e233549a4549d2c346472fb8f97de02eb01ecfcf91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c683b49fbbf45125413c67f40e1653f6b4682245a3266f7bf600d0ac1b9406b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbef9fcbbcaaba85642f80363e9eb5cc5d7b561be4b8d218629dba98142919c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="metadataPublish")
    def metadata_publish(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataPublish"))

    @metadata_publish.setter
    def metadata_publish(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7f07add026e3e222f1e34d8b38bef62447dcf19bf5bf854a0f405a8e3463f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataPublish", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e20850ed4b5c4b743323e03d1df81cde2ac98207e5803c9bca59c290482afb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.authServerScope.AuthServerScopeConfig",
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
        "name": "name",
        "consent": "consent",
        "default": "default",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "metadata_publish": "metadataPublish",
    },
)
class AuthServerScopeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        consent: typing.Optional[builtins.str] = None,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata_publish: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auth_server_id: Auth server ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#auth_server_id AuthServerScope#auth_server_id}
        :param name: Auth server scope name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#name AuthServerScope#name}
        :param consent: EA Feature and thus it is simply ignored if the feature is off. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#consent AuthServerScope#consent}
        :param default: A default scope will be returned in an access token when the client omits the scope parameter in a token request, provided this scope is allowed as part of the access policy rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#default AuthServerScope#default}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#description AuthServerScope#description}.
        :param display_name: Name of the end user displayed in a consent dialog box. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#display_name AuthServerScope#display_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#id AuthServerScope#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata_publish: Whether to publish metadata or not, matching API type despite the fact it could just be a boolean. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#metadata_publish AuthServerScope#metadata_publish}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544e4177fa89c47be858bff85d743da6ac76f255ec74fd25c568c941a1a0bac6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auth_server_id", value=auth_server_id, expected_type=type_hints["auth_server_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument consent", value=consent, expected_type=type_hints["consent"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metadata_publish", value=metadata_publish, expected_type=type_hints["metadata_publish"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_server_id": auth_server_id,
            "name": name,
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
        if consent is not None:
            self._values["consent"] = consent
        if default is not None:
            self._values["default"] = default
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if metadata_publish is not None:
            self._values["metadata_publish"] = metadata_publish

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#auth_server_id AuthServerScope#auth_server_id}
        '''
        result = self._values.get("auth_server_id")
        assert result is not None, "Required property 'auth_server_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Auth server scope name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#name AuthServerScope#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consent(self) -> typing.Optional[builtins.str]:
        '''EA Feature and thus it is simply ignored if the feature is off.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#consent AuthServerScope#consent}
        '''
        result = self._values.get("consent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A default scope will be returned in an access token when the client omits the scope parameter in a token request, provided this scope is allowed as part of the access policy rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#default AuthServerScope#default}
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#description AuthServerScope#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Name of the end user displayed in a consent dialog box.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#display_name AuthServerScope#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#id AuthServerScope#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_publish(self) -> typing.Optional[builtins.str]:
        '''Whether to publish metadata or not, matching API type despite the fact it could just be a boolean.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_scope#metadata_publish AuthServerScope#metadata_publish}
        '''
        result = self._values.get("metadata_publish")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthServerScopeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AuthServerScope",
    "AuthServerScopeConfig",
]

publication.publish()

def _typecheckingstub__c25e7b90d2ad183108cc9094b2acf1910236937c2a20d4ea539b047677e02683(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auth_server_id: builtins.str,
    name: builtins.str,
    consent: typing.Optional[builtins.str] = None,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata_publish: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d6e3ad33ccab21ed3da6b69604cf36301cbd1a82bdeebae3403a7db722cf97fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e505fb5d0049e482cedcf5bc3a19b10f03683a4f6e73faeff5b3902e78fd14b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed708b172240fed145d48a3d5c4fe753988e75899a705e3f329809a2721762b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b49982b35a51b969913b1e233549a4549d2c346472fb8f97de02eb01ecfcf91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c683b49fbbf45125413c67f40e1653f6b4682245a3266f7bf600d0ac1b9406b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbef9fcbbcaaba85642f80363e9eb5cc5d7b561be4b8d218629dba98142919c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7f07add026e3e222f1e34d8b38bef62447dcf19bf5bf854a0f405a8e3463f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e20850ed4b5c4b743323e03d1df81cde2ac98207e5803c9bca59c290482afb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544e4177fa89c47be858bff85d743da6ac76f255ec74fd25c568c941a1a0bac6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_server_id: builtins.str,
    name: builtins.str,
    consent: typing.Optional[builtins.str] = None,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata_publish: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
