'''
# `vault_kmip_secret_backend`

Refer to the Terraform Registory for docs: [`vault_kmip_secret_backend`](https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend).
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


class KmipSecretBackend(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.kmipSecretBackend.KmipSecretBackend",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend vault_kmip_secret_backend}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        path: builtins.str,
        default_tls_client_key_bits: typing.Optional[jsii.Number] = None,
        default_tls_client_key_type: typing.Optional[builtins.str] = None,
        default_tls_client_ttl: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        listen_addrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        server_hostnames: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls_ca_key_bits: typing.Optional[jsii.Number] = None,
        tls_ca_key_type: typing.Optional[builtins.str] = None,
        tls_min_version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend vault_kmip_secret_backend} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param path: Path where KMIP secret backend will be mounted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#path KmipSecretBackend#path}
        :param default_tls_client_key_bits: Client certificate key bits, valid values depend on key type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_key_bits KmipSecretBackend#default_tls_client_key_bits}
        :param default_tls_client_key_type: Client certificate key type, rsa or ec. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_key_type KmipSecretBackend#default_tls_client_key_type}
        :param default_tls_client_ttl: Client certificate TTL in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_ttl KmipSecretBackend#default_tls_client_ttl}
        :param description: Human-friendly description of the mount for the backend. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#description KmipSecretBackend#description}
        :param disable_remount: If set, opts out of mount migration on path updates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#disable_remount KmipSecretBackend#disable_remount}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#id KmipSecretBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param listen_addrs: Addresses the KMIP server should listen on (host:port). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#listen_addrs KmipSecretBackend#listen_addrs}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#namespace KmipSecretBackend#namespace}
        :param server_hostnames: Hostnames to include in the server's TLS certificate as SAN DNS names. The first will be used as the common name (CN) Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#server_hostnames KmipSecretBackend#server_hostnames}
        :param server_ips: IPs to include in the server's TLS certificate as SAN IP addresses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#server_ips KmipSecretBackend#server_ips}
        :param tls_ca_key_bits: CA key bits, valid values depend on key type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_ca_key_bits KmipSecretBackend#tls_ca_key_bits}
        :param tls_ca_key_type: CA key type, rsa or ec. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_ca_key_type KmipSecretBackend#tls_ca_key_type}
        :param tls_min_version: Minimum TLS version to accept. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_min_version KmipSecretBackend#tls_min_version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f1cd19672cd534fbe2c663ed130e68e1e5d6c4c568f62919c3e110aa1cc1c1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KmipSecretBackendConfig(
            path=path,
            default_tls_client_key_bits=default_tls_client_key_bits,
            default_tls_client_key_type=default_tls_client_key_type,
            default_tls_client_ttl=default_tls_client_ttl,
            description=description,
            disable_remount=disable_remount,
            id=id,
            listen_addrs=listen_addrs,
            namespace=namespace,
            server_hostnames=server_hostnames,
            server_ips=server_ips,
            tls_ca_key_bits=tls_ca_key_bits,
            tls_ca_key_type=tls_ca_key_type,
            tls_min_version=tls_min_version,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetDefaultTlsClientKeyBits")
    def reset_default_tls_client_key_bits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTlsClientKeyBits", []))

    @jsii.member(jsii_name="resetDefaultTlsClientKeyType")
    def reset_default_tls_client_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTlsClientKeyType", []))

    @jsii.member(jsii_name="resetDefaultTlsClientTtl")
    def reset_default_tls_client_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTlsClientTtl", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableRemount")
    def reset_disable_remount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableRemount", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetListenAddrs")
    def reset_listen_addrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetListenAddrs", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetServerHostnames")
    def reset_server_hostnames(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerHostnames", []))

    @jsii.member(jsii_name="resetServerIps")
    def reset_server_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerIps", []))

    @jsii.member(jsii_name="resetTlsCaKeyBits")
    def reset_tls_ca_key_bits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsCaKeyBits", []))

    @jsii.member(jsii_name="resetTlsCaKeyType")
    def reset_tls_ca_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsCaKeyType", []))

    @jsii.member(jsii_name="resetTlsMinVersion")
    def reset_tls_min_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsMinVersion", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="defaultTlsClientKeyBitsInput")
    def default_tls_client_key_bits_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTlsClientKeyBitsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTlsClientKeyTypeInput")
    def default_tls_client_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTlsClientKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTlsClientTtlInput")
    def default_tls_client_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTlsClientTtlInput"))

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
    @jsii.member(jsii_name="listenAddrsInput")
    def listen_addrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "listenAddrsInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="serverHostnamesInput")
    def server_hostnames_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serverHostnamesInput"))

    @builtins.property
    @jsii.member(jsii_name="serverIpsInput")
    def server_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serverIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCaKeyBitsInput")
    def tls_ca_key_bits_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tlsCaKeyBitsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCaKeyTypeInput")
    def tls_ca_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsCaKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsMinVersionInput")
    def tls_min_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsMinVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTlsClientKeyBits")
    def default_tls_client_key_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTlsClientKeyBits"))

    @default_tls_client_key_bits.setter
    def default_tls_client_key_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff036ec0e20f47ced6d93934d2695f57bb84ffe13dba2f77dd12a034c5e9575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTlsClientKeyBits", value)

    @builtins.property
    @jsii.member(jsii_name="defaultTlsClientKeyType")
    def default_tls_client_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTlsClientKeyType"))

    @default_tls_client_key_type.setter
    def default_tls_client_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af475a60885b969dc7818778d02584a49ac8df3769cb397f08f05b958b198d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTlsClientKeyType", value)

    @builtins.property
    @jsii.member(jsii_name="defaultTlsClientTtl")
    def default_tls_client_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTlsClientTtl"))

    @default_tls_client_ttl.setter
    def default_tls_client_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592440d62d6abc4d0741e4f443374a8f978071dcfbc09c6e6ed216407b7ffedc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTlsClientTtl", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aad70a890ce92193a8d0dd82270135b005aa50d110ec911725cb1e2f9ce0a7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__061f6428de2b6323d842ab63f4bf34032300720309654debdc8bbb1c8e14a330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableRemount", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3e1e6638e19b4dd9087d975abc54dcae9ab350aec66cd781a17a7a741eee40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="listenAddrs")
    def listen_addrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "listenAddrs"))

    @listen_addrs.setter
    def listen_addrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22684210561bbaca2855f6a2913b2d7332243b969520c8d909612b8338a4c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenAddrs", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7f4695c59a222065aae0f8ba8c17ec94234710390935f73fc527a143fa85e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04690898e76823e1a2645ff4bc73a3a3a4556cd41dbb60fe6e55602b6e07bf7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="serverHostnames")
    def server_hostnames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serverHostnames"))

    @server_hostnames.setter
    def server_hostnames(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efcb587161a3888d3997c532570e424b364c2086a4480280111d2b82ce6bbec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverHostnames", value)

    @builtins.property
    @jsii.member(jsii_name="serverIps")
    def server_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serverIps"))

    @server_ips.setter
    def server_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f167cb974e7b56937e43212d06c98cd1de0821e56110ab45b7293e4a4caf42e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverIps", value)

    @builtins.property
    @jsii.member(jsii_name="tlsCaKeyBits")
    def tls_ca_key_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tlsCaKeyBits"))

    @tls_ca_key_bits.setter
    def tls_ca_key_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf82afbd0f3e999b9880afda66f157a57517c73fa9fef397ea675b34f428096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsCaKeyBits", value)

    @builtins.property
    @jsii.member(jsii_name="tlsCaKeyType")
    def tls_ca_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsCaKeyType"))

    @tls_ca_key_type.setter
    def tls_ca_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218ea8dde21b19b2e69337e4e68e63e6d893113a43604b7d79bd4d0a71b81fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsCaKeyType", value)

    @builtins.property
    @jsii.member(jsii_name="tlsMinVersion")
    def tls_min_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsMinVersion"))

    @tls_min_version.setter
    def tls_min_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679c4c97a02ed58c9dda44f60a57e4ece99e827e7882728d694f235aa53efdac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsMinVersion", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.kmipSecretBackend.KmipSecretBackendConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "path": "path",
        "default_tls_client_key_bits": "defaultTlsClientKeyBits",
        "default_tls_client_key_type": "defaultTlsClientKeyType",
        "default_tls_client_ttl": "defaultTlsClientTtl",
        "description": "description",
        "disable_remount": "disableRemount",
        "id": "id",
        "listen_addrs": "listenAddrs",
        "namespace": "namespace",
        "server_hostnames": "serverHostnames",
        "server_ips": "serverIps",
        "tls_ca_key_bits": "tlsCaKeyBits",
        "tls_ca_key_type": "tlsCaKeyType",
        "tls_min_version": "tlsMinVersion",
    },
)
class KmipSecretBackendConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        path: builtins.str,
        default_tls_client_key_bits: typing.Optional[jsii.Number] = None,
        default_tls_client_key_type: typing.Optional[builtins.str] = None,
        default_tls_client_ttl: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        listen_addrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        server_hostnames: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls_ca_key_bits: typing.Optional[jsii.Number] = None,
        tls_ca_key_type: typing.Optional[builtins.str] = None,
        tls_min_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param path: Path where KMIP secret backend will be mounted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#path KmipSecretBackend#path}
        :param default_tls_client_key_bits: Client certificate key bits, valid values depend on key type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_key_bits KmipSecretBackend#default_tls_client_key_bits}
        :param default_tls_client_key_type: Client certificate key type, rsa or ec. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_key_type KmipSecretBackend#default_tls_client_key_type}
        :param default_tls_client_ttl: Client certificate TTL in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_ttl KmipSecretBackend#default_tls_client_ttl}
        :param description: Human-friendly description of the mount for the backend. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#description KmipSecretBackend#description}
        :param disable_remount: If set, opts out of mount migration on path updates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#disable_remount KmipSecretBackend#disable_remount}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#id KmipSecretBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param listen_addrs: Addresses the KMIP server should listen on (host:port). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#listen_addrs KmipSecretBackend#listen_addrs}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#namespace KmipSecretBackend#namespace}
        :param server_hostnames: Hostnames to include in the server's TLS certificate as SAN DNS names. The first will be used as the common name (CN) Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#server_hostnames KmipSecretBackend#server_hostnames}
        :param server_ips: IPs to include in the server's TLS certificate as SAN IP addresses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#server_ips KmipSecretBackend#server_ips}
        :param tls_ca_key_bits: CA key bits, valid values depend on key type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_ca_key_bits KmipSecretBackend#tls_ca_key_bits}
        :param tls_ca_key_type: CA key type, rsa or ec. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_ca_key_type KmipSecretBackend#tls_ca_key_type}
        :param tls_min_version: Minimum TLS version to accept. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_min_version KmipSecretBackend#tls_min_version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2661d7f66687c235e6528187932cf3e5adda35eee7fafa4f220c49762126919)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument default_tls_client_key_bits", value=default_tls_client_key_bits, expected_type=type_hints["default_tls_client_key_bits"])
            check_type(argname="argument default_tls_client_key_type", value=default_tls_client_key_type, expected_type=type_hints["default_tls_client_key_type"])
            check_type(argname="argument default_tls_client_ttl", value=default_tls_client_ttl, expected_type=type_hints["default_tls_client_ttl"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_remount", value=disable_remount, expected_type=type_hints["disable_remount"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument listen_addrs", value=listen_addrs, expected_type=type_hints["listen_addrs"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument server_hostnames", value=server_hostnames, expected_type=type_hints["server_hostnames"])
            check_type(argname="argument server_ips", value=server_ips, expected_type=type_hints["server_ips"])
            check_type(argname="argument tls_ca_key_bits", value=tls_ca_key_bits, expected_type=type_hints["tls_ca_key_bits"])
            check_type(argname="argument tls_ca_key_type", value=tls_ca_key_type, expected_type=type_hints["tls_ca_key_type"])
            check_type(argname="argument tls_min_version", value=tls_min_version, expected_type=type_hints["tls_min_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
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
        if default_tls_client_key_bits is not None:
            self._values["default_tls_client_key_bits"] = default_tls_client_key_bits
        if default_tls_client_key_type is not None:
            self._values["default_tls_client_key_type"] = default_tls_client_key_type
        if default_tls_client_ttl is not None:
            self._values["default_tls_client_ttl"] = default_tls_client_ttl
        if description is not None:
            self._values["description"] = description
        if disable_remount is not None:
            self._values["disable_remount"] = disable_remount
        if id is not None:
            self._values["id"] = id
        if listen_addrs is not None:
            self._values["listen_addrs"] = listen_addrs
        if namespace is not None:
            self._values["namespace"] = namespace
        if server_hostnames is not None:
            self._values["server_hostnames"] = server_hostnames
        if server_ips is not None:
            self._values["server_ips"] = server_ips
        if tls_ca_key_bits is not None:
            self._values["tls_ca_key_bits"] = tls_ca_key_bits
        if tls_ca_key_type is not None:
            self._values["tls_ca_key_type"] = tls_ca_key_type
        if tls_min_version is not None:
            self._values["tls_min_version"] = tls_min_version

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
    def path(self) -> builtins.str:
        '''Path where KMIP secret backend will be mounted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#path KmipSecretBackend#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_tls_client_key_bits(self) -> typing.Optional[jsii.Number]:
        '''Client certificate key bits, valid values depend on key type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_key_bits KmipSecretBackend#default_tls_client_key_bits}
        '''
        result = self._values.get("default_tls_client_key_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_tls_client_key_type(self) -> typing.Optional[builtins.str]:
        '''Client certificate key type, rsa or ec.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_key_type KmipSecretBackend#default_tls_client_key_type}
        '''
        result = self._values.get("default_tls_client_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_tls_client_ttl(self) -> typing.Optional[jsii.Number]:
        '''Client certificate TTL in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#default_tls_client_ttl KmipSecretBackend#default_tls_client_ttl}
        '''
        result = self._values.get("default_tls_client_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Human-friendly description of the mount for the backend.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#description KmipSecretBackend#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_remount(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, opts out of mount migration on path updates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#disable_remount KmipSecretBackend#disable_remount}
        '''
        result = self._values.get("disable_remount")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#id KmipSecretBackend#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def listen_addrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Addresses the KMIP server should listen on (host:port).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#listen_addrs KmipSecretBackend#listen_addrs}
        '''
        result = self._values.get("listen_addrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Target namespace. (requires Enterprise).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#namespace KmipSecretBackend#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_hostnames(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Hostnames to include in the server's TLS certificate as SAN DNS names.

        The first will be used as the common name (CN)

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#server_hostnames KmipSecretBackend#server_hostnames}
        '''
        result = self._values.get("server_hostnames")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def server_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IPs to include in the server's TLS certificate as SAN IP addresses.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#server_ips KmipSecretBackend#server_ips}
        '''
        result = self._values.get("server_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls_ca_key_bits(self) -> typing.Optional[jsii.Number]:
        '''CA key bits, valid values depend on key type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_ca_key_bits KmipSecretBackend#tls_ca_key_bits}
        '''
        result = self._values.get("tls_ca_key_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_ca_key_type(self) -> typing.Optional[builtins.str]:
        '''CA key type, rsa or ec.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_ca_key_type KmipSecretBackend#tls_ca_key_type}
        '''
        result = self._values.get("tls_ca_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_min_version(self) -> typing.Optional[builtins.str]:
        '''Minimum TLS version to accept.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/kmip_secret_backend#tls_min_version KmipSecretBackend#tls_min_version}
        '''
        result = self._values.get("tls_min_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmipSecretBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "KmipSecretBackend",
    "KmipSecretBackendConfig",
]

publication.publish()

def _typecheckingstub__d0f1cd19672cd534fbe2c663ed130e68e1e5d6c4c568f62919c3e110aa1cc1c1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    path: builtins.str,
    default_tls_client_key_bits: typing.Optional[jsii.Number] = None,
    default_tls_client_key_type: typing.Optional[builtins.str] = None,
    default_tls_client_ttl: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    listen_addrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    server_hostnames: typing.Optional[typing.Sequence[builtins.str]] = None,
    server_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_ca_key_bits: typing.Optional[jsii.Number] = None,
    tls_ca_key_type: typing.Optional[builtins.str] = None,
    tls_min_version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__dff036ec0e20f47ced6d93934d2695f57bb84ffe13dba2f77dd12a034c5e9575(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af475a60885b969dc7818778d02584a49ac8df3769cb397f08f05b958b198d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592440d62d6abc4d0741e4f443374a8f978071dcfbc09c6e6ed216407b7ffedc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aad70a890ce92193a8d0dd82270135b005aa50d110ec911725cb1e2f9ce0a7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061f6428de2b6323d842ab63f4bf34032300720309654debdc8bbb1c8e14a330(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3e1e6638e19b4dd9087d975abc54dcae9ab350aec66cd781a17a7a741eee40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22684210561bbaca2855f6a2913b2d7332243b969520c8d909612b8338a4c2e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7f4695c59a222065aae0f8ba8c17ec94234710390935f73fc527a143fa85e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04690898e76823e1a2645ff4bc73a3a3a4556cd41dbb60fe6e55602b6e07bf7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efcb587161a3888d3997c532570e424b364c2086a4480280111d2b82ce6bbec6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f167cb974e7b56937e43212d06c98cd1de0821e56110ab45b7293e4a4caf42e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf82afbd0f3e999b9880afda66f157a57517c73fa9fef397ea675b34f428096(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218ea8dde21b19b2e69337e4e68e63e6d893113a43604b7d79bd4d0a71b81fad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679c4c97a02ed58c9dda44f60a57e4ece99e827e7882728d694f235aa53efdac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2661d7f66687c235e6528187932cf3e5adda35eee7fafa4f220c49762126919(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: builtins.str,
    default_tls_client_key_bits: typing.Optional[jsii.Number] = None,
    default_tls_client_key_type: typing.Optional[builtins.str] = None,
    default_tls_client_ttl: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    listen_addrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    server_hostnames: typing.Optional[typing.Sequence[builtins.str]] = None,
    server_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_ca_key_bits: typing.Optional[jsii.Number] = None,
    tls_ca_key_type: typing.Optional[builtins.str] = None,
    tls_min_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
