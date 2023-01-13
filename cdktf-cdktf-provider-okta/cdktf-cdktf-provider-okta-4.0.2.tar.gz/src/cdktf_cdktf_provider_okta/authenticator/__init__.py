'''
# `okta_authenticator`

Refer to the Terraform Registory for docs: [`okta_authenticator`](https://www.terraform.io/docs/providers/okta/r/authenticator).
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


class Authenticator(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.authenticator.Authenticator",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/authenticator okta_authenticator}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        provider_auth_port: typing.Optional[jsii.Number] = None,
        provider_host: typing.Optional[builtins.str] = None,
        provider_hostname: typing.Optional[builtins.str] = None,
        provider_integration_key: typing.Optional[builtins.str] = None,
        provider_json: typing.Optional[builtins.str] = None,
        provider_secret_key: typing.Optional[builtins.str] = None,
        provider_shared_secret: typing.Optional[builtins.str] = None,
        provider_user_name_template: typing.Optional[builtins.str] = None,
        settings: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/authenticator okta_authenticator} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key: A human-readable string that identifies the Authenticator. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#key Authenticator#key}
        :param name: Display name of the Authenticator. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#name Authenticator#name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#id Authenticator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param provider_auth_port: The RADIUS server port (for example 1812). This is defined when the On-Prem RADIUS server is configured. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_auth_port Authenticator#provider_auth_port}
        :param provider_host: The Duo Security API hostname. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_host Authenticator#provider_host}
        :param provider_hostname: Server host name or IP address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_hostname Authenticator#provider_hostname}
        :param provider_integration_key: The Duo Security integration key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_integration_key Authenticator#provider_integration_key}
        :param provider_json: Provider in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_json Authenticator#provider_json}
        :param provider_secret_key: The Duo Security secret key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_secret_key Authenticator#provider_secret_key}
        :param provider_shared_secret: An authentication key that must be defined when the RADIUS server is configured, and must be the same on both the RADIUS client and server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_shared_secret Authenticator#provider_shared_secret}
        :param provider_user_name_template: Format expected by the provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_user_name_template Authenticator#provider_user_name_template}
        :param settings: Authenticator settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#settings Authenticator#settings}
        :param status: Authenticator status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#status Authenticator#status}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91999b5ceaa9fd8adbb7c9b082825b73e7710d9a8663d9db9a804d1fc70a7862)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AuthenticatorConfig(
            key=key,
            name=name,
            id=id,
            provider_auth_port=provider_auth_port,
            provider_host=provider_host,
            provider_hostname=provider_hostname,
            provider_integration_key=provider_integration_key,
            provider_json=provider_json,
            provider_secret_key=provider_secret_key,
            provider_shared_secret=provider_shared_secret,
            provider_user_name_template=provider_user_name_template,
            settings=settings,
            status=status,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProviderAuthPort")
    def reset_provider_auth_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderAuthPort", []))

    @jsii.member(jsii_name="resetProviderHost")
    def reset_provider_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderHost", []))

    @jsii.member(jsii_name="resetProviderHostname")
    def reset_provider_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderHostname", []))

    @jsii.member(jsii_name="resetProviderIntegrationKey")
    def reset_provider_integration_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderIntegrationKey", []))

    @jsii.member(jsii_name="resetProviderJson")
    def reset_provider_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderJson", []))

    @jsii.member(jsii_name="resetProviderSecretKey")
    def reset_provider_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderSecretKey", []))

    @jsii.member(jsii_name="resetProviderSharedSecret")
    def reset_provider_shared_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderSharedSecret", []))

    @jsii.member(jsii_name="resetProviderUserNameTemplate")
    def reset_provider_user_name_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderUserNameTemplate", []))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="providerInstanceId")
    def provider_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerInstanceId"))

    @builtins.property
    @jsii.member(jsii_name="providerType")
    def provider_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerType"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerAuthPortInput")
    def provider_auth_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "providerAuthPortInput"))

    @builtins.property
    @jsii.member(jsii_name="providerHostInput")
    def provider_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerHostInput"))

    @builtins.property
    @jsii.member(jsii_name="providerHostnameInput")
    def provider_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerIntegrationKeyInput")
    def provider_integration_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerIntegrationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="providerJsonInput")
    def provider_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="providerSecretKeyInput")
    def provider_secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerSecretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="providerSharedSecretInput")
    def provider_shared_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerSharedSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="providerUserNameTemplateInput")
    def provider_user_name_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerUserNameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f6365c282ec11f258264cf3abaa0a011603c98cb44e2cd79c0721050290dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad04569846f5abf23d4bbdc9f4cd3f8ea1c4978f01b645513e88832f69eb1b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9817153f7d04c794405ee265be0ca7eb5273806e5c0ffcc71f60ca868f2db203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="providerAuthPort")
    def provider_auth_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "providerAuthPort"))

    @provider_auth_port.setter
    def provider_auth_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0883f696206a65b1961d681afb24fb0527db7ab69c031403eadd59fddb372b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerAuthPort", value)

    @builtins.property
    @jsii.member(jsii_name="providerHost")
    def provider_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerHost"))

    @provider_host.setter
    def provider_host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2cc87dfd6fa4761efac293706402dc79f84f5d7d31b0595224be889f7b0197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerHost", value)

    @builtins.property
    @jsii.member(jsii_name="providerHostname")
    def provider_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerHostname"))

    @provider_hostname.setter
    def provider_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131e382e51a6d685e628b7440b31e8c5a8830ab119190c68e9cd01c55b1ac844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerHostname", value)

    @builtins.property
    @jsii.member(jsii_name="providerIntegrationKey")
    def provider_integration_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerIntegrationKey"))

    @provider_integration_key.setter
    def provider_integration_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6ae9dd9138c354b0b73760433fe6979593bbfe4e61715d2b2939ae82af39d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerIntegrationKey", value)

    @builtins.property
    @jsii.member(jsii_name="providerJson")
    def provider_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerJson"))

    @provider_json.setter
    def provider_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1718de4b2b3b8d5e9fecfa342d62ce9400b4538eb34f9bda09e1112b6557d98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerJson", value)

    @builtins.property
    @jsii.member(jsii_name="providerSecretKey")
    def provider_secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerSecretKey"))

    @provider_secret_key.setter
    def provider_secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1b2d55fe6fbbddd9a4af9016749bdf51ad14bca4ee92ac207da8a25ed2e413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerSecretKey", value)

    @builtins.property
    @jsii.member(jsii_name="providerSharedSecret")
    def provider_shared_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerSharedSecret"))

    @provider_shared_secret.setter
    def provider_shared_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d51ca8c9b76b1315f04ec1e27a2aa811a81fbf578f889dec7a9ab7f5cc15059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerSharedSecret", value)

    @builtins.property
    @jsii.member(jsii_name="providerUserNameTemplate")
    def provider_user_name_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerUserNameTemplate"))

    @provider_user_name_template.setter
    def provider_user_name_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34acff97937fc7f8c69f155f4cd3e93c7e55a46c73cbd8c93709684e60409516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerUserNameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "settings"))

    @settings.setter
    def settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae27a08993c92b899e3336fa2fca4e20a0da90af13159b61cc8bace1e552ed26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "settings", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9defb4193ba54f76455a0ebe032daf22088af469f72cfb4f19baa8b062c6aed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.authenticator.AuthenticatorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key": "key",
        "name": "name",
        "id": "id",
        "provider_auth_port": "providerAuthPort",
        "provider_host": "providerHost",
        "provider_hostname": "providerHostname",
        "provider_integration_key": "providerIntegrationKey",
        "provider_json": "providerJson",
        "provider_secret_key": "providerSecretKey",
        "provider_shared_secret": "providerSharedSecret",
        "provider_user_name_template": "providerUserNameTemplate",
        "settings": "settings",
        "status": "status",
    },
)
class AuthenticatorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        provider_auth_port: typing.Optional[jsii.Number] = None,
        provider_host: typing.Optional[builtins.str] = None,
        provider_hostname: typing.Optional[builtins.str] = None,
        provider_integration_key: typing.Optional[builtins.str] = None,
        provider_json: typing.Optional[builtins.str] = None,
        provider_secret_key: typing.Optional[builtins.str] = None,
        provider_shared_secret: typing.Optional[builtins.str] = None,
        provider_user_name_template: typing.Optional[builtins.str] = None,
        settings: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key: A human-readable string that identifies the Authenticator. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#key Authenticator#key}
        :param name: Display name of the Authenticator. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#name Authenticator#name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#id Authenticator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param provider_auth_port: The RADIUS server port (for example 1812). This is defined when the On-Prem RADIUS server is configured. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_auth_port Authenticator#provider_auth_port}
        :param provider_host: The Duo Security API hostname. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_host Authenticator#provider_host}
        :param provider_hostname: Server host name or IP address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_hostname Authenticator#provider_hostname}
        :param provider_integration_key: The Duo Security integration key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_integration_key Authenticator#provider_integration_key}
        :param provider_json: Provider in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_json Authenticator#provider_json}
        :param provider_secret_key: The Duo Security secret key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_secret_key Authenticator#provider_secret_key}
        :param provider_shared_secret: An authentication key that must be defined when the RADIUS server is configured, and must be the same on both the RADIUS client and server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_shared_secret Authenticator#provider_shared_secret}
        :param provider_user_name_template: Format expected by the provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_user_name_template Authenticator#provider_user_name_template}
        :param settings: Authenticator settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#settings Authenticator#settings}
        :param status: Authenticator status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#status Authenticator#status}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ff90991c73cb4c1f3430b0c4729e67abf297946da35af876d445dfc9b94aa9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument provider_auth_port", value=provider_auth_port, expected_type=type_hints["provider_auth_port"])
            check_type(argname="argument provider_host", value=provider_host, expected_type=type_hints["provider_host"])
            check_type(argname="argument provider_hostname", value=provider_hostname, expected_type=type_hints["provider_hostname"])
            check_type(argname="argument provider_integration_key", value=provider_integration_key, expected_type=type_hints["provider_integration_key"])
            check_type(argname="argument provider_json", value=provider_json, expected_type=type_hints["provider_json"])
            check_type(argname="argument provider_secret_key", value=provider_secret_key, expected_type=type_hints["provider_secret_key"])
            check_type(argname="argument provider_shared_secret", value=provider_shared_secret, expected_type=type_hints["provider_shared_secret"])
            check_type(argname="argument provider_user_name_template", value=provider_user_name_template, expected_type=type_hints["provider_user_name_template"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
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
        if id is not None:
            self._values["id"] = id
        if provider_auth_port is not None:
            self._values["provider_auth_port"] = provider_auth_port
        if provider_host is not None:
            self._values["provider_host"] = provider_host
        if provider_hostname is not None:
            self._values["provider_hostname"] = provider_hostname
        if provider_integration_key is not None:
            self._values["provider_integration_key"] = provider_integration_key
        if provider_json is not None:
            self._values["provider_json"] = provider_json
        if provider_secret_key is not None:
            self._values["provider_secret_key"] = provider_secret_key
        if provider_shared_secret is not None:
            self._values["provider_shared_secret"] = provider_shared_secret
        if provider_user_name_template is not None:
            self._values["provider_user_name_template"] = provider_user_name_template
        if settings is not None:
            self._values["settings"] = settings
        if status is not None:
            self._values["status"] = status

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
    def key(self) -> builtins.str:
        '''A human-readable string that identifies the Authenticator.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#key Authenticator#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Display name of the Authenticator.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#name Authenticator#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#id Authenticator#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_auth_port(self) -> typing.Optional[jsii.Number]:
        '''The RADIUS server port (for example 1812). This is defined when the On-Prem RADIUS server is configured.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_auth_port Authenticator#provider_auth_port}
        '''
        result = self._values.get("provider_auth_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provider_host(self) -> typing.Optional[builtins.str]:
        '''The Duo Security API hostname.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_host Authenticator#provider_host}
        '''
        result = self._values.get("provider_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_hostname(self) -> typing.Optional[builtins.str]:
        '''Server host name or IP address.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_hostname Authenticator#provider_hostname}
        '''
        result = self._values.get("provider_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_integration_key(self) -> typing.Optional[builtins.str]:
        '''The Duo Security integration key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_integration_key Authenticator#provider_integration_key}
        '''
        result = self._values.get("provider_integration_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_json(self) -> typing.Optional[builtins.str]:
        '''Provider in JSON format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_json Authenticator#provider_json}
        '''
        result = self._values.get("provider_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_secret_key(self) -> typing.Optional[builtins.str]:
        '''The Duo Security secret key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_secret_key Authenticator#provider_secret_key}
        '''
        result = self._values.get("provider_secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_shared_secret(self) -> typing.Optional[builtins.str]:
        '''An authentication key that must be defined when the RADIUS server is configured, and must be the same on both the RADIUS client and server.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_shared_secret Authenticator#provider_shared_secret}
        '''
        result = self._values.get("provider_shared_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_user_name_template(self) -> typing.Optional[builtins.str]:
        '''Format expected by the provider.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#provider_user_name_template Authenticator#provider_user_name_template}
        '''
        result = self._values.get("provider_user_name_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def settings(self) -> typing.Optional[builtins.str]:
        '''Authenticator settings in JSON format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#settings Authenticator#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Authenticator status: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/authenticator#status Authenticator#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthenticatorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Authenticator",
    "AuthenticatorConfig",
]

publication.publish()

def _typecheckingstub__91999b5ceaa9fd8adbb7c9b082825b73e7710d9a8663d9db9a804d1fc70a7862(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    provider_auth_port: typing.Optional[jsii.Number] = None,
    provider_host: typing.Optional[builtins.str] = None,
    provider_hostname: typing.Optional[builtins.str] = None,
    provider_integration_key: typing.Optional[builtins.str] = None,
    provider_json: typing.Optional[builtins.str] = None,
    provider_secret_key: typing.Optional[builtins.str] = None,
    provider_shared_secret: typing.Optional[builtins.str] = None,
    provider_user_name_template: typing.Optional[builtins.str] = None,
    settings: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__26f6365c282ec11f258264cf3abaa0a011603c98cb44e2cd79c0721050290dcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad04569846f5abf23d4bbdc9f4cd3f8ea1c4978f01b645513e88832f69eb1b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9817153f7d04c794405ee265be0ca7eb5273806e5c0ffcc71f60ca868f2db203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0883f696206a65b1961d681afb24fb0527db7ab69c031403eadd59fddb372b5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2cc87dfd6fa4761efac293706402dc79f84f5d7d31b0595224be889f7b0197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131e382e51a6d685e628b7440b31e8c5a8830ab119190c68e9cd01c55b1ac844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6ae9dd9138c354b0b73760433fe6979593bbfe4e61715d2b2939ae82af39d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1718de4b2b3b8d5e9fecfa342d62ce9400b4538eb34f9bda09e1112b6557d98b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1b2d55fe6fbbddd9a4af9016749bdf51ad14bca4ee92ac207da8a25ed2e413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d51ca8c9b76b1315f04ec1e27a2aa811a81fbf578f889dec7a9ab7f5cc15059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34acff97937fc7f8c69f155f4cd3e93c7e55a46c73cbd8c93709684e60409516(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae27a08993c92b899e3336fa2fca4e20a0da90af13159b61cc8bace1e552ed26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9defb4193ba54f76455a0ebe032daf22088af469f72cfb4f19baa8b062c6aed2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ff90991c73cb4c1f3430b0c4729e67abf297946da35af876d445dfc9b94aa9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    provider_auth_port: typing.Optional[jsii.Number] = None,
    provider_host: typing.Optional[builtins.str] = None,
    provider_hostname: typing.Optional[builtins.str] = None,
    provider_integration_key: typing.Optional[builtins.str] = None,
    provider_json: typing.Optional[builtins.str] = None,
    provider_secret_key: typing.Optional[builtins.str] = None,
    provider_shared_secret: typing.Optional[builtins.str] = None,
    provider_user_name_template: typing.Optional[builtins.str] = None,
    settings: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
