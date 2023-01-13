'''
# `spotinst_multai_listener`

Refer to the Terraform Registory for docs: [`spotinst_multai_listener`](https://www.terraform.io/docs/providers/spotinst/r/multai_listener).
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


class MultaiListener(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiListener.MultaiListener",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener spotinst_multai_listener}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        balancer_id: builtins.str,
        port: jsii.Number,
        protocol: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiListenerTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tls_config: typing.Optional[typing.Union["MultaiListenerTlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener spotinst_multai_listener} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param balancer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#balancer_id MultaiListener#balancer_id}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#port MultaiListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#protocol MultaiListener#protocol}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#id MultaiListener#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#tags MultaiListener#tags}
        :param tls_config: tls_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#tls_config MultaiListener#tls_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9baf31f76a9a02f2d4da0eb4648c55562388077d88aa11f6301e3203382f5f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MultaiListenerConfig(
            balancer_id=balancer_id,
            port=port,
            protocol=protocol,
            id=id,
            tags=tags,
            tls_config=tls_config,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiListenerTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7b656ce4dc289f5406ac00ce6ba548372b9bccdf0dc1370064ffb39cb3ad1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="putTlsConfig")
    def put_tls_config(
        self,
        *,
        certificate_ids: typing.Sequence[builtins.str],
        cipher_suites: typing.Sequence[builtins.str],
        max_version: builtins.str,
        min_version: builtins.str,
        prefer_server_cipher_suites: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        session_tickets_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param certificate_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#certificate_ids MultaiListener#certificate_ids}.
        :param cipher_suites: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#cipher_suites MultaiListener#cipher_suites}.
        :param max_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#max_version MultaiListener#max_version}.
        :param min_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#min_version MultaiListener#min_version}.
        :param prefer_server_cipher_suites: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#prefer_server_cipher_suites MultaiListener#prefer_server_cipher_suites}.
        :param session_tickets_disabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#session_tickets_disabled MultaiListener#session_tickets_disabled}.
        '''
        value = MultaiListenerTlsConfig(
            certificate_ids=certificate_ids,
            cipher_suites=cipher_suites,
            max_version=max_version,
            min_version=min_version,
            prefer_server_cipher_suites=prefer_server_cipher_suites,
            session_tickets_disabled=session_tickets_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putTlsConfig", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTlsConfig")
    def reset_tls_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsConfig", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "MultaiListenerTagsList":
        return typing.cast("MultaiListenerTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="tlsConfig")
    def tls_config(self) -> "MultaiListenerTlsConfigOutputReference":
        return typing.cast("MultaiListenerTlsConfigOutputReference", jsii.get(self, "tlsConfig"))

    @builtins.property
    @jsii.member(jsii_name="balancerIdInput")
    def balancer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "balancerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiListenerTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiListenerTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsConfigInput")
    def tls_config_input(self) -> typing.Optional["MultaiListenerTlsConfig"]:
        return typing.cast(typing.Optional["MultaiListenerTlsConfig"], jsii.get(self, "tlsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="balancerId")
    def balancer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "balancerId"))

    @balancer_id.setter
    def balancer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83e97ace3c2a0798e37bf345ae14fc175d88de5d58c350316d672c5bc8349e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "balancerId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06406b7eab992f942f05a5588a76f652e33eeb1c269bd25dc876a2c4b09f4ac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baa5267ca003f18d8e9ede88c732d71cda29e88bc59ff633eda8183debb75c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7615efaab90af168ee3498b470e2249d4abc2c36dac564d559f78172ebdb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.multaiListener.MultaiListenerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "balancer_id": "balancerId",
        "port": "port",
        "protocol": "protocol",
        "id": "id",
        "tags": "tags",
        "tls_config": "tlsConfig",
    },
)
class MultaiListenerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        balancer_id: builtins.str,
        port: jsii.Number,
        protocol: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiListenerTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tls_config: typing.Optional[typing.Union["MultaiListenerTlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param balancer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#balancer_id MultaiListener#balancer_id}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#port MultaiListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#protocol MultaiListener#protocol}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#id MultaiListener#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#tags MultaiListener#tags}
        :param tls_config: tls_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#tls_config MultaiListener#tls_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(tls_config, dict):
            tls_config = MultaiListenerTlsConfig(**tls_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddbe03ec961160214b22dcb59999cb0cbfeb2a475a850bb1b9e15a3b205e5dc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument balancer_id", value=balancer_id, expected_type=type_hints["balancer_id"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tls_config", value=tls_config, expected_type=type_hints["tls_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "balancer_id": balancer_id,
            "port": port,
            "protocol": protocol,
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
        if tags is not None:
            self._values["tags"] = tags
        if tls_config is not None:
            self._values["tls_config"] = tls_config

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
    def balancer_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#balancer_id MultaiListener#balancer_id}.'''
        result = self._values.get("balancer_id")
        assert result is not None, "Required property 'balancer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#port MultaiListener#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#protocol MultaiListener#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#id MultaiListener#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiListenerTags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#tags MultaiListener#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiListenerTags"]]], result)

    @builtins.property
    def tls_config(self) -> typing.Optional["MultaiListenerTlsConfig"]:
        '''tls_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#tls_config MultaiListener#tls_config}
        '''
        result = self._values.get("tls_config")
        return typing.cast(typing.Optional["MultaiListenerTlsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultaiListenerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.multaiListener.MultaiListenerTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class MultaiListenerTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#key MultaiListener#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#value MultaiListener#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673b7a5424e3cf0def4c2796fbc86d0620618f080305b05250e4994c2520704a)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#key MultaiListener#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#value MultaiListener#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultaiListenerTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MultaiListenerTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiListener.MultaiListenerTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f465e3a7148569fa4051af9fe3bfd9e88897371698b0c026fea8170224b4271c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MultaiListenerTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff62040c26195c0dd2fea6f630f725e44606ad0aef485562af40ae97bf532ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MultaiListenerTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1691473d86e8f02d1b245ae3cd598e1b9a2efe8d26e1be635634e4e5e133569d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__742552415ca7c971ccd34a36321b0a165b5f254d645cdb47d670dc0793555df8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a073edf39c3f24f346ddb15b461b193c773a84f1a4e37506785b4fde4b493cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiListenerTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiListenerTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiListenerTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deffc50db96776d4db54799382a8eb5249a3430535e0430fd4d0aa1634947584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MultaiListenerTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiListener.MultaiListenerTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09948030d874481b01eef584e4cb4e39f7831b95ce3b60bbacf41b2cff6e0843)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9144d91f653447d961b6e15e48f4c3584da6e8eb4cf1db8879cd427db936a410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd4b4823c852260e858e8af5229ff31b4f51382c91e718c7b8b6c3254179cb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MultaiListenerTags, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MultaiListenerTags, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MultaiListenerTags, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c915310f1ec080ea338a13181feee316240fdb7efd02820e82a9480503653548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.multaiListener.MultaiListenerTlsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_ids": "certificateIds",
        "cipher_suites": "cipherSuites",
        "max_version": "maxVersion",
        "min_version": "minVersion",
        "prefer_server_cipher_suites": "preferServerCipherSuites",
        "session_tickets_disabled": "sessionTicketsDisabled",
    },
)
class MultaiListenerTlsConfig:
    def __init__(
        self,
        *,
        certificate_ids: typing.Sequence[builtins.str],
        cipher_suites: typing.Sequence[builtins.str],
        max_version: builtins.str,
        min_version: builtins.str,
        prefer_server_cipher_suites: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        session_tickets_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param certificate_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#certificate_ids MultaiListener#certificate_ids}.
        :param cipher_suites: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#cipher_suites MultaiListener#cipher_suites}.
        :param max_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#max_version MultaiListener#max_version}.
        :param min_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#min_version MultaiListener#min_version}.
        :param prefer_server_cipher_suites: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#prefer_server_cipher_suites MultaiListener#prefer_server_cipher_suites}.
        :param session_tickets_disabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#session_tickets_disabled MultaiListener#session_tickets_disabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d8822463f4439856193104a0d15f52a5e39958dc4097cd4f5bf425d4bb2a03)
            check_type(argname="argument certificate_ids", value=certificate_ids, expected_type=type_hints["certificate_ids"])
            check_type(argname="argument cipher_suites", value=cipher_suites, expected_type=type_hints["cipher_suites"])
            check_type(argname="argument max_version", value=max_version, expected_type=type_hints["max_version"])
            check_type(argname="argument min_version", value=min_version, expected_type=type_hints["min_version"])
            check_type(argname="argument prefer_server_cipher_suites", value=prefer_server_cipher_suites, expected_type=type_hints["prefer_server_cipher_suites"])
            check_type(argname="argument session_tickets_disabled", value=session_tickets_disabled, expected_type=type_hints["session_tickets_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_ids": certificate_ids,
            "cipher_suites": cipher_suites,
            "max_version": max_version,
            "min_version": min_version,
            "prefer_server_cipher_suites": prefer_server_cipher_suites,
            "session_tickets_disabled": session_tickets_disabled,
        }

    @builtins.property
    def certificate_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#certificate_ids MultaiListener#certificate_ids}.'''
        result = self._values.get("certificate_ids")
        assert result is not None, "Required property 'certificate_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cipher_suites(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#cipher_suites MultaiListener#cipher_suites}.'''
        result = self._values.get("cipher_suites")
        assert result is not None, "Required property 'cipher_suites' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def max_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#max_version MultaiListener#max_version}.'''
        result = self._values.get("max_version")
        assert result is not None, "Required property 'max_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def min_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#min_version MultaiListener#min_version}.'''
        result = self._values.get("min_version")
        assert result is not None, "Required property 'min_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefer_server_cipher_suites(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#prefer_server_cipher_suites MultaiListener#prefer_server_cipher_suites}.'''
        result = self._values.get("prefer_server_cipher_suites")
        assert result is not None, "Required property 'prefer_server_cipher_suites' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def session_tickets_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_listener#session_tickets_disabled MultaiListener#session_tickets_disabled}.'''
        result = self._values.get("session_tickets_disabled")
        assert result is not None, "Required property 'session_tickets_disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultaiListenerTlsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MultaiListenerTlsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiListener.MultaiListenerTlsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f28026483280f80bee8e5e4e6ff330975d6d80d700dcb3dee7ab4b4bc57ad1e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateIdsInput")
    def certificate_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cipherSuitesInput")
    def cipher_suites_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cipherSuitesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxVersionInput")
    def max_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="minVersionInput")
    def min_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="preferServerCipherSuitesInput")
    def prefer_server_cipher_suites_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preferServerCipherSuitesInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTicketsDisabledInput")
    def session_tickets_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionTicketsDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateIds")
    def certificate_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificateIds"))

    @certificate_ids.setter
    def certificate_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d890bd4ef1decbcbe547072a751f7c42e5969416a876b95a86638377bbdddf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateIds", value)

    @builtins.property
    @jsii.member(jsii_name="cipherSuites")
    def cipher_suites(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cipherSuites"))

    @cipher_suites.setter
    def cipher_suites(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907f4d53140ebb7d03cf49d9345236a3e3e357ed899fe88f0b76bf30c9508820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cipherSuites", value)

    @builtins.property
    @jsii.member(jsii_name="maxVersion")
    def max_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxVersion"))

    @max_version.setter
    def max_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf49fde638fb1da6a9e8847205f543fb6819b380a408fd0150115918666e760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxVersion", value)

    @builtins.property
    @jsii.member(jsii_name="minVersion")
    def min_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minVersion"))

    @min_version.setter
    def min_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba5803feb5f2a613136c04f2d5d87e7f0aa243b97c2d13344aafb39cc0ae74d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minVersion", value)

    @builtins.property
    @jsii.member(jsii_name="preferServerCipherSuites")
    def prefer_server_cipher_suites(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preferServerCipherSuites"))

    @prefer_server_cipher_suites.setter
    def prefer_server_cipher_suites(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5cddf7253ade19440288e3389a2763c2349865b3948c36d524b863d93daf4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferServerCipherSuites", value)

    @builtins.property
    @jsii.member(jsii_name="sessionTicketsDisabled")
    def session_tickets_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sessionTicketsDisabled"))

    @session_tickets_disabled.setter
    def session_tickets_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03c60a7bf9ed3fb222eeaf0fa63ed01fecfd82e8e56058beeb33807ffe9e5e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTicketsDisabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MultaiListenerTlsConfig]:
        return typing.cast(typing.Optional[MultaiListenerTlsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MultaiListenerTlsConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7ec9b9858d8d9be10acf03bd552b3cd342dd1e1f3de3b8790161a7ba794f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MultaiListener",
    "MultaiListenerConfig",
    "MultaiListenerTags",
    "MultaiListenerTagsList",
    "MultaiListenerTagsOutputReference",
    "MultaiListenerTlsConfig",
    "MultaiListenerTlsConfigOutputReference",
]

publication.publish()

def _typecheckingstub__d9baf31f76a9a02f2d4da0eb4648c55562388077d88aa11f6301e3203382f5f8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    balancer_id: builtins.str,
    port: jsii.Number,
    protocol: builtins.str,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiListenerTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tls_config: typing.Optional[typing.Union[MultaiListenerTlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8e7b656ce4dc289f5406ac00ce6ba548372b9bccdf0dc1370064ffb39cb3ad1f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiListenerTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83e97ace3c2a0798e37bf345ae14fc175d88de5d58c350316d672c5bc8349e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06406b7eab992f942f05a5588a76f652e33eeb1c269bd25dc876a2c4b09f4ac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baa5267ca003f18d8e9ede88c732d71cda29e88bc59ff633eda8183debb75c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7615efaab90af168ee3498b470e2249d4abc2c36dac564d559f78172ebdb68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddbe03ec961160214b22dcb59999cb0cbfeb2a475a850bb1b9e15a3b205e5dc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    balancer_id: builtins.str,
    port: jsii.Number,
    protocol: builtins.str,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiListenerTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tls_config: typing.Optional[typing.Union[MultaiListenerTlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673b7a5424e3cf0def4c2796fbc86d0620618f080305b05250e4994c2520704a(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f465e3a7148569fa4051af9fe3bfd9e88897371698b0c026fea8170224b4271c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff62040c26195c0dd2fea6f630f725e44606ad0aef485562af40ae97bf532ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1691473d86e8f02d1b245ae3cd598e1b9a2efe8d26e1be635634e4e5e133569d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742552415ca7c971ccd34a36321b0a165b5f254d645cdb47d670dc0793555df8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a073edf39c3f24f346ddb15b461b193c773a84f1a4e37506785b4fde4b493cfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deffc50db96776d4db54799382a8eb5249a3430535e0430fd4d0aa1634947584(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiListenerTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09948030d874481b01eef584e4cb4e39f7831b95ce3b60bbacf41b2cff6e0843(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9144d91f653447d961b6e15e48f4c3584da6e8eb4cf1db8879cd427db936a410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd4b4823c852260e858e8af5229ff31b4f51382c91e718c7b8b6c3254179cb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c915310f1ec080ea338a13181feee316240fdb7efd02820e82a9480503653548(
    value: typing.Optional[typing.Union[MultaiListenerTags, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d8822463f4439856193104a0d15f52a5e39958dc4097cd4f5bf425d4bb2a03(
    *,
    certificate_ids: typing.Sequence[builtins.str],
    cipher_suites: typing.Sequence[builtins.str],
    max_version: builtins.str,
    min_version: builtins.str,
    prefer_server_cipher_suites: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    session_tickets_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28026483280f80bee8e5e4e6ff330975d6d80d700dcb3dee7ab4b4bc57ad1e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d890bd4ef1decbcbe547072a751f7c42e5969416a876b95a86638377bbdddf2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907f4d53140ebb7d03cf49d9345236a3e3e357ed899fe88f0b76bf30c9508820(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf49fde638fb1da6a9e8847205f543fb6819b380a408fd0150115918666e760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba5803feb5f2a613136c04f2d5d87e7f0aa243b97c2d13344aafb39cc0ae74d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5cddf7253ade19440288e3389a2763c2349865b3948c36d524b863d93daf4d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03c60a7bf9ed3fb222eeaf0fa63ed01fecfd82e8e56058beeb33807ffe9e5e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7ec9b9858d8d9be10acf03bd552b3cd342dd1e1f3de3b8790161a7ba794f44(
    value: typing.Optional[MultaiListenerTlsConfig],
) -> None:
    """Type checking stubs"""
    pass
