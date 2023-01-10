'''
# `vault_gcp_auth_backend`

Refer to the Terraform Registory for docs: [`vault_gcp_auth_backend`](https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend).
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


class GcpAuthBackend(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.gcpAuthBackend.GcpAuthBackend",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend vault_gcp_auth_backend}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        client_email: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        custom_endpoint: typing.Optional[typing.Union["GcpAuthBackendCustomEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        namespace: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        private_key_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend vault_gcp_auth_backend} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#client_email GcpAuthBackend#client_email}.
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#client_id GcpAuthBackend#client_id}.
        :param credentials: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#credentials GcpAuthBackend#credentials}.
        :param custom_endpoint: custom_endpoint block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#custom_endpoint GcpAuthBackend#custom_endpoint}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#description GcpAuthBackend#description}.
        :param disable_remount: If set, opts out of mount migration on path updates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#disable_remount GcpAuthBackend#disable_remount}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#id GcpAuthBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local: Specifies if the auth method is local only. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#local GcpAuthBackend#local}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#namespace GcpAuthBackend#namespace}
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#path GcpAuthBackend#path}.
        :param private_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#private_key_id GcpAuthBackend#private_key_id}.
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#project_id GcpAuthBackend#project_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea57e35d7aaa26c96ffb109b024b2ef1490e5351aa930d0b6c379a9a7b043c3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GcpAuthBackendConfig(
            client_email=client_email,
            client_id=client_id,
            credentials=credentials,
            custom_endpoint=custom_endpoint,
            description=description,
            disable_remount=disable_remount,
            id=id,
            local=local,
            namespace=namespace,
            path=path,
            private_key_id=private_key_id,
            project_id=project_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCustomEndpoint")
    def put_custom_endpoint(
        self,
        *,
        api: typing.Optional[builtins.str] = None,
        compute: typing.Optional[builtins.str] = None,
        crm: typing.Optional[builtins.str] = None,
        iam: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api: Replaces the service endpoint used in API requests to https://www.googleapis.com. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#api GcpAuthBackend#api}
        :param compute: Replaces the service endpoint used in API requests to ``https://compute.googleapis.com``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#compute GcpAuthBackend#compute}
        :param crm: Replaces the service endpoint used in API requests to ``https://cloudresourcemanager.googleapis.com``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#crm GcpAuthBackend#crm}
        :param iam: Replaces the service endpoint used in API requests to ``https://iam.googleapis.com``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#iam GcpAuthBackend#iam}
        '''
        value = GcpAuthBackendCustomEndpoint(
            api=api, compute=compute, crm=crm, iam=iam
        )

        return typing.cast(None, jsii.invoke(self, "putCustomEndpoint", [value]))

    @jsii.member(jsii_name="resetClientEmail")
    def reset_client_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientEmail", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetCustomEndpoint")
    def reset_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomEndpoint", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableRemount")
    def reset_disable_remount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableRemount", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocal")
    def reset_local(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocal", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPrivateKeyId")
    def reset_private_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="customEndpoint")
    def custom_endpoint(self) -> "GcpAuthBackendCustomEndpointOutputReference":
        return typing.cast("GcpAuthBackendCustomEndpointOutputReference", jsii.get(self, "customEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="clientEmailInput")
    def client_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="customEndpointInput")
    def custom_endpoint_input(self) -> typing.Optional["GcpAuthBackendCustomEndpoint"]:
        return typing.cast(typing.Optional["GcpAuthBackendCustomEndpoint"], jsii.get(self, "customEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableRemountInput")
    def disable_remount_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableRemountInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localInput")
    def local_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyIdInput")
    def private_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientEmail")
    def client_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientEmail"))

    @client_email.setter
    def client_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa5e551a1d12a3178b07144854dfe1f7572f2ef531903aefe09f3db8d544b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientEmail", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e484ea98bbdb861d24dcc83e29c46723f0809f3c56c1ef17af0b0517cb712f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ef2ae5ed459a8a0a27f4708fa00456b37c3935e9b7c68add4abf1345a421bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc225de2b9d91cc1619fa62d7d5026fdf6684cd77349588387448ce7fdb93eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableRemount")
    def disable_remount(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableRemount"))

    @disable_remount.setter
    def disable_remount(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765aaed94214c0b0d23e309bd7bf8dcdbcf52a7daadc0087531a3b705dd8e3b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableRemount", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f120e4092111afee6047856d2da10b452ffa852b43ede255a469fbcfe99a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="local")
    def local(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "local"))

    @local.setter
    def local(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c9f021dc062a54e83b35fca39a0fc9f82bd04f5b2d5b5eb54226fb7a163dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "local", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82d4bbadd8a71a3ebe31b11be2ed3552c8cbe4c546e61aed7310d66eb51a4ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d0b0b3753ce803838855536fccd0cb980da94084c8364b00909c13c72b6cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="privateKeyId")
    def private_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyId"))

    @private_key_id.setter
    def private_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58546750ff9bdfd98ced060885089ebf76fb7a1b1e986cf41ce85417c1fe085c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b60809fc53a34346873f3ba8ec4cb5458f775cc894d929dee82ca70f2a7b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.gcpAuthBackend.GcpAuthBackendConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "client_email": "clientEmail",
        "client_id": "clientId",
        "credentials": "credentials",
        "custom_endpoint": "customEndpoint",
        "description": "description",
        "disable_remount": "disableRemount",
        "id": "id",
        "local": "local",
        "namespace": "namespace",
        "path": "path",
        "private_key_id": "privateKeyId",
        "project_id": "projectId",
    },
)
class GcpAuthBackendConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_email: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        custom_endpoint: typing.Optional[typing.Union["GcpAuthBackendCustomEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        namespace: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        private_key_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param client_email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#client_email GcpAuthBackend#client_email}.
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#client_id GcpAuthBackend#client_id}.
        :param credentials: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#credentials GcpAuthBackend#credentials}.
        :param custom_endpoint: custom_endpoint block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#custom_endpoint GcpAuthBackend#custom_endpoint}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#description GcpAuthBackend#description}.
        :param disable_remount: If set, opts out of mount migration on path updates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#disable_remount GcpAuthBackend#disable_remount}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#id GcpAuthBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local: Specifies if the auth method is local only. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#local GcpAuthBackend#local}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#namespace GcpAuthBackend#namespace}
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#path GcpAuthBackend#path}.
        :param private_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#private_key_id GcpAuthBackend#private_key_id}.
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#project_id GcpAuthBackend#project_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_endpoint, dict):
            custom_endpoint = GcpAuthBackendCustomEndpoint(**custom_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ac29f0beffb6b8c99a3151a11c1904758cb9a3f1b0cd2a696cf03e97736790)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument client_email", value=client_email, expected_type=type_hints["client_email"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument custom_endpoint", value=custom_endpoint, expected_type=type_hints["custom_endpoint"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_remount", value=disable_remount, expected_type=type_hints["disable_remount"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument private_key_id", value=private_key_id, expected_type=type_hints["private_key_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if client_email is not None:
            self._values["client_email"] = client_email
        if client_id is not None:
            self._values["client_id"] = client_id
        if credentials is not None:
            self._values["credentials"] = credentials
        if custom_endpoint is not None:
            self._values["custom_endpoint"] = custom_endpoint
        if description is not None:
            self._values["description"] = description
        if disable_remount is not None:
            self._values["disable_remount"] = disable_remount
        if id is not None:
            self._values["id"] = id
        if local is not None:
            self._values["local"] = local
        if namespace is not None:
            self._values["namespace"] = namespace
        if path is not None:
            self._values["path"] = path
        if private_key_id is not None:
            self._values["private_key_id"] = private_key_id
        if project_id is not None:
            self._values["project_id"] = project_id

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
    def client_email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#client_email GcpAuthBackend#client_email}.'''
        result = self._values.get("client_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#client_id GcpAuthBackend#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#credentials GcpAuthBackend#credentials}.'''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_endpoint(self) -> typing.Optional["GcpAuthBackendCustomEndpoint"]:
        '''custom_endpoint block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#custom_endpoint GcpAuthBackend#custom_endpoint}
        '''
        result = self._values.get("custom_endpoint")
        return typing.cast(typing.Optional["GcpAuthBackendCustomEndpoint"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#description GcpAuthBackend#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_remount(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, opts out of mount migration on path updates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#disable_remount GcpAuthBackend#disable_remount}
        '''
        result = self._values.get("disable_remount")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#id GcpAuthBackend#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the auth method is local only.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#local GcpAuthBackend#local}
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Target namespace. (requires Enterprise).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#namespace GcpAuthBackend#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#path GcpAuthBackend#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#private_key_id GcpAuthBackend#private_key_id}.'''
        result = self._values.get("private_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#project_id GcpAuthBackend#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GcpAuthBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.gcpAuthBackend.GcpAuthBackendCustomEndpoint",
    jsii_struct_bases=[],
    name_mapping={"api": "api", "compute": "compute", "crm": "crm", "iam": "iam"},
)
class GcpAuthBackendCustomEndpoint:
    def __init__(
        self,
        *,
        api: typing.Optional[builtins.str] = None,
        compute: typing.Optional[builtins.str] = None,
        crm: typing.Optional[builtins.str] = None,
        iam: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api: Replaces the service endpoint used in API requests to https://www.googleapis.com. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#api GcpAuthBackend#api}
        :param compute: Replaces the service endpoint used in API requests to ``https://compute.googleapis.com``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#compute GcpAuthBackend#compute}
        :param crm: Replaces the service endpoint used in API requests to ``https://cloudresourcemanager.googleapis.com``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#crm GcpAuthBackend#crm}
        :param iam: Replaces the service endpoint used in API requests to ``https://iam.googleapis.com``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#iam GcpAuthBackend#iam}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__022512fcb42009b980ddbdb29ddcb66c0b0e50d104c2bb6d972b703711421a66)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument compute", value=compute, expected_type=type_hints["compute"])
            check_type(argname="argument crm", value=crm, expected_type=type_hints["crm"])
            check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api is not None:
            self._values["api"] = api
        if compute is not None:
            self._values["compute"] = compute
        if crm is not None:
            self._values["crm"] = crm
        if iam is not None:
            self._values["iam"] = iam

    @builtins.property
    def api(self) -> typing.Optional[builtins.str]:
        '''Replaces the service endpoint used in API requests to https://www.googleapis.com.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#api GcpAuthBackend#api}
        '''
        result = self._values.get("api")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute(self) -> typing.Optional[builtins.str]:
        '''Replaces the service endpoint used in API requests to ``https://compute.googleapis.com``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#compute GcpAuthBackend#compute}
        '''
        result = self._values.get("compute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def crm(self) -> typing.Optional[builtins.str]:
        '''Replaces the service endpoint used in API requests to ``https://cloudresourcemanager.googleapis.com``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#crm GcpAuthBackend#crm}
        '''
        result = self._values.get("crm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam(self) -> typing.Optional[builtins.str]:
        '''Replaces the service endpoint used in API requests to ``https://iam.googleapis.com``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/gcp_auth_backend#iam GcpAuthBackend#iam}
        '''
        result = self._values.get("iam")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GcpAuthBackendCustomEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GcpAuthBackendCustomEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.gcpAuthBackend.GcpAuthBackendCustomEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54dfa33806e6e15553e45d55a1578b09910c6e87d3efe0063407fe3cbf8bfce8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApi")
    def reset_api(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApi", []))

    @jsii.member(jsii_name="resetCompute")
    def reset_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompute", []))

    @jsii.member(jsii_name="resetCrm")
    def reset_crm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrm", []))

    @jsii.member(jsii_name="resetIam")
    def reset_iam(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIam", []))

    @builtins.property
    @jsii.member(jsii_name="apiInput")
    def api_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiInput"))

    @builtins.property
    @jsii.member(jsii_name="computeInput")
    def compute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeInput"))

    @builtins.property
    @jsii.member(jsii_name="crmInput")
    def crm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crmInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInput")
    def iam_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamInput"))

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "api"))

    @api.setter
    def api(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433dde81601e0957f1ff34d338be5cbd9cf88353288c520030a2db9840201a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "api", value)

    @builtins.property
    @jsii.member(jsii_name="compute")
    def compute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compute"))

    @compute.setter
    def compute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75894dd8e441aa1b784be402b111544e5b3a2a27daa4aaa12eac870b63545d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compute", value)

    @builtins.property
    @jsii.member(jsii_name="crm")
    def crm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crm"))

    @crm.setter
    def crm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4536b68bb9dc59d6d3bdd7f28906d74a254667a84a91c50e61ee8954106fc4a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crm", value)

    @builtins.property
    @jsii.member(jsii_name="iam")
    def iam(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iam"))

    @iam.setter
    def iam(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b637f1cb2123388d4819de2e59db7af47efe777964c4a0de8c126a79690929ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iam", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GcpAuthBackendCustomEndpoint]:
        return typing.cast(typing.Optional[GcpAuthBackendCustomEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GcpAuthBackendCustomEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b38a1f37aefa5c998ce1c6d080a327eb91dd1e77735aa9283d4179553d3c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GcpAuthBackend",
    "GcpAuthBackendConfig",
    "GcpAuthBackendCustomEndpoint",
    "GcpAuthBackendCustomEndpointOutputReference",
]

publication.publish()

def _typecheckingstub__ea57e35d7aaa26c96ffb109b024b2ef1490e5351aa930d0b6c379a9a7b043c3c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    client_email: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[builtins.str] = None,
    custom_endpoint: typing.Optional[typing.Union[GcpAuthBackendCustomEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    namespace: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    private_key_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__afa5e551a1d12a3178b07144854dfe1f7572f2ef531903aefe09f3db8d544b24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e484ea98bbdb861d24dcc83e29c46723f0809f3c56c1ef17af0b0517cb712f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ef2ae5ed459a8a0a27f4708fa00456b37c3935e9b7c68add4abf1345a421bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc225de2b9d91cc1619fa62d7d5026fdf6684cd77349588387448ce7fdb93eda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765aaed94214c0b0d23e309bd7bf8dcdbcf52a7daadc0087531a3b705dd8e3b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f120e4092111afee6047856d2da10b452ffa852b43ede255a469fbcfe99a47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c9f021dc062a54e83b35fca39a0fc9f82bd04f5b2d5b5eb54226fb7a163dba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82d4bbadd8a71a3ebe31b11be2ed3552c8cbe4c546e61aed7310d66eb51a4ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d0b0b3753ce803838855536fccd0cb980da94084c8364b00909c13c72b6cd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58546750ff9bdfd98ced060885089ebf76fb7a1b1e986cf41ce85417c1fe085c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b60809fc53a34346873f3ba8ec4cb5458f775cc894d929dee82ca70f2a7b15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ac29f0beffb6b8c99a3151a11c1904758cb9a3f1b0cd2a696cf03e97736790(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_email: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[builtins.str] = None,
    custom_endpoint: typing.Optional[typing.Union[GcpAuthBackendCustomEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    namespace: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    private_key_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022512fcb42009b980ddbdb29ddcb66c0b0e50d104c2bb6d972b703711421a66(
    *,
    api: typing.Optional[builtins.str] = None,
    compute: typing.Optional[builtins.str] = None,
    crm: typing.Optional[builtins.str] = None,
    iam: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54dfa33806e6e15553e45d55a1578b09910c6e87d3efe0063407fe3cbf8bfce8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433dde81601e0957f1ff34d338be5cbd9cf88353288c520030a2db9840201a6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75894dd8e441aa1b784be402b111544e5b3a2a27daa4aaa12eac870b63545d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4536b68bb9dc59d6d3bdd7f28906d74a254667a84a91c50e61ee8954106fc4a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b637f1cb2123388d4819de2e59db7af47efe777964c4a0de8c126a79690929ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b38a1f37aefa5c998ce1c6d080a327eb91dd1e77735aa9283d4179553d3c46(
    value: typing.Optional[GcpAuthBackendCustomEndpoint],
) -> None:
    """Type checking stubs"""
    pass
