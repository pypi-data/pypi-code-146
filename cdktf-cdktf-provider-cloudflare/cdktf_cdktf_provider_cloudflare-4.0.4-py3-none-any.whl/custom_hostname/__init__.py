'''
# `cloudflare_custom_hostname`

Refer to the Terraform Registory for docs: [`cloudflare_custom_hostname`](https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname).
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


class CustomHostname(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostname",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname cloudflare_custom_hostname}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hostname: builtins.str,
        zone_id: builtins.str,
        custom_metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        custom_origin_server: typing.Optional[builtins.str] = None,
        custom_origin_sni: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ssl: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomHostnameSsl", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wait_for_ssl_pending_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname cloudflare_custom_hostname} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hostname: Hostname you intend to request a certificate for. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#hostname CustomHostname#hostname}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#zone_id CustomHostname#zone_id}
        :param custom_metadata: Custom metadata associated with custom hostname. Only supports primitive string values, all other values are accessible via the API directly. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_metadata CustomHostname#custom_metadata}
        :param custom_origin_server: The custom origin server used for certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_origin_server CustomHostname#custom_origin_server}
        :param custom_origin_sni: The `custom origin SNI <https://developers.cloudflare.com/ssl/ssl-for-saas/hostname-specific-behavior/custom-origin>`_ used for certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_origin_sni CustomHostname#custom_origin_sni}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#id CustomHostname#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#ssl CustomHostname#ssl}
        :param wait_for_ssl_pending_validation: Whether to wait for a custom hostname SSL sub-object to reach status ``pending_validation`` during creation. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#wait_for_ssl_pending_validation CustomHostname#wait_for_ssl_pending_validation}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2999243784abde236613791702b528a1f4896b54dcf17adba234a389d1841b3d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CustomHostnameConfig(
            hostname=hostname,
            zone_id=zone_id,
            custom_metadata=custom_metadata,
            custom_origin_server=custom_origin_server,
            custom_origin_sni=custom_origin_sni,
            id=id,
            ssl=ssl,
            wait_for_ssl_pending_validation=wait_for_ssl_pending_validation,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putSsl")
    def put_ssl(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomHostnameSsl", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514d078b168b29e240b271bc89ee703186a68c6e59c20e8286f3dd99c0cbe73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSsl", [value]))

    @jsii.member(jsii_name="resetCustomMetadata")
    def reset_custom_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMetadata", []))

    @jsii.member(jsii_name="resetCustomOriginServer")
    def reset_custom_origin_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomOriginServer", []))

    @jsii.member(jsii_name="resetCustomOriginSni")
    def reset_custom_origin_sni(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomOriginSni", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSsl")
    def reset_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsl", []))

    @jsii.member(jsii_name="resetWaitForSslPendingValidation")
    def reset_wait_for_ssl_pending_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForSslPendingValidation", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="ownershipVerification")
    def ownership_verification(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "ownershipVerification"))

    @builtins.property
    @jsii.member(jsii_name="ownershipVerificationHttp")
    def ownership_verification_http(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "ownershipVerificationHttp"))

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(self) -> "CustomHostnameSslList":
        return typing.cast("CustomHostnameSslList", jsii.get(self, "ssl"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="customMetadataInput")
    def custom_metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="customOriginServerInput")
    def custom_origin_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customOriginServerInput"))

    @builtins.property
    @jsii.member(jsii_name="customOriginSniInput")
    def custom_origin_sni_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customOriginSniInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="sslInput")
    def ssl_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomHostnameSsl"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomHostnameSsl"]]], jsii.get(self, "sslInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForSslPendingValidationInput")
    def wait_for_ssl_pending_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForSslPendingValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customMetadata")
    def custom_metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customMetadata"))

    @custom_metadata.setter
    def custom_metadata(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de637288db3c09f8cabeb56459d8d32edce0ca73cf35b168a739e59a09c8f11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customMetadata", value)

    @builtins.property
    @jsii.member(jsii_name="customOriginServer")
    def custom_origin_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customOriginServer"))

    @custom_origin_server.setter
    def custom_origin_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02076b152f8b46094262d0027dfc930a81477e4f6a717130f57de2ac269c0a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customOriginServer", value)

    @builtins.property
    @jsii.member(jsii_name="customOriginSni")
    def custom_origin_sni(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customOriginSni"))

    @custom_origin_sni.setter
    def custom_origin_sni(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec17de835603301487ab088d7c0b1e989e68675fc038ca2dc41f555e5256987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customOriginSni", value)

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363b224feee645a6e9d647a4835702b51ad748047425bfa39d8ec804c062a95b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623289f22fb0d206aee353a5a4dd281fc2e7791c35363b498d84a98de18f3f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="waitForSslPendingValidation")
    def wait_for_ssl_pending_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForSslPendingValidation"))

    @wait_for_ssl_pending_validation.setter
    def wait_for_ssl_pending_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b9435597feb457896f7afd402b35f240e355b385e30f087afb4c298373500b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForSslPendingValidation", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f5ec58ac1d08057ceabff7f21b9fe0ead80236bfe3a796dba741f79d7f3777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hostname": "hostname",
        "zone_id": "zoneId",
        "custom_metadata": "customMetadata",
        "custom_origin_server": "customOriginServer",
        "custom_origin_sni": "customOriginSni",
        "id": "id",
        "ssl": "ssl",
        "wait_for_ssl_pending_validation": "waitForSslPendingValidation",
    },
)
class CustomHostnameConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hostname: builtins.str,
        zone_id: builtins.str,
        custom_metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        custom_origin_server: typing.Optional[builtins.str] = None,
        custom_origin_sni: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ssl: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomHostnameSsl", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wait_for_ssl_pending_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hostname: Hostname you intend to request a certificate for. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#hostname CustomHostname#hostname}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#zone_id CustomHostname#zone_id}
        :param custom_metadata: Custom metadata associated with custom hostname. Only supports primitive string values, all other values are accessible via the API directly. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_metadata CustomHostname#custom_metadata}
        :param custom_origin_server: The custom origin server used for certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_origin_server CustomHostname#custom_origin_server}
        :param custom_origin_sni: The `custom origin SNI <https://developers.cloudflare.com/ssl/ssl-for-saas/hostname-specific-behavior/custom-origin>`_ used for certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_origin_sni CustomHostname#custom_origin_sni}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#id CustomHostname#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#ssl CustomHostname#ssl}
        :param wait_for_ssl_pending_validation: Whether to wait for a custom hostname SSL sub-object to reach status ``pending_validation`` during creation. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#wait_for_ssl_pending_validation CustomHostname#wait_for_ssl_pending_validation}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92de60c9769d9bcda063e9f820f1972e69185c791f003143b549bdc4352855b2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument custom_metadata", value=custom_metadata, expected_type=type_hints["custom_metadata"])
            check_type(argname="argument custom_origin_server", value=custom_origin_server, expected_type=type_hints["custom_origin_server"])
            check_type(argname="argument custom_origin_sni", value=custom_origin_sni, expected_type=type_hints["custom_origin_sni"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ssl", value=ssl, expected_type=type_hints["ssl"])
            check_type(argname="argument wait_for_ssl_pending_validation", value=wait_for_ssl_pending_validation, expected_type=type_hints["wait_for_ssl_pending_validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
            "zone_id": zone_id,
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
        if custom_metadata is not None:
            self._values["custom_metadata"] = custom_metadata
        if custom_origin_server is not None:
            self._values["custom_origin_server"] = custom_origin_server
        if custom_origin_sni is not None:
            self._values["custom_origin_sni"] = custom_origin_sni
        if id is not None:
            self._values["id"] = id
        if ssl is not None:
            self._values["ssl"] = ssl
        if wait_for_ssl_pending_validation is not None:
            self._values["wait_for_ssl_pending_validation"] = wait_for_ssl_pending_validation

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
    def hostname(self) -> builtins.str:
        '''Hostname you intend to request a certificate for. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#hostname CustomHostname#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#zone_id CustomHostname#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_metadata(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom metadata associated with custom hostname.

        Only supports primitive string values, all other values are accessible via the API directly.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_metadata CustomHostname#custom_metadata}
        '''
        result = self._values.get("custom_metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def custom_origin_server(self) -> typing.Optional[builtins.str]:
        '''The custom origin server used for certificates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_origin_server CustomHostname#custom_origin_server}
        '''
        result = self._values.get("custom_origin_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_origin_sni(self) -> typing.Optional[builtins.str]:
        '''The `custom origin SNI <https://developers.cloudflare.com/ssl/ssl-for-saas/hostname-specific-behavior/custom-origin>`_ used for certificates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_origin_sni CustomHostname#custom_origin_sni}
        '''
        result = self._values.get("custom_origin_sni")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#id CustomHostname#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomHostnameSsl"]]]:
        '''ssl block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#ssl CustomHostname#ssl}
        '''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomHostnameSsl"]]], result)

    @builtins.property
    def wait_for_ssl_pending_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to wait for a custom hostname SSL sub-object to reach status ``pending_validation`` during creation. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#wait_for_ssl_pending_validation CustomHostname#wait_for_ssl_pending_validation}
        '''
        result = self._values.get("wait_for_ssl_pending_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomHostnameConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSsl",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority": "certificateAuthority",
        "custom_certificate": "customCertificate",
        "custom_key": "customKey",
        "method": "method",
        "settings": "settings",
        "type": "type",
        "wildcard": "wildcard",
    },
)
class CustomHostnameSsl:
    def __init__(
        self,
        *,
        certificate_authority: typing.Optional[builtins.str] = None,
        custom_certificate: typing.Optional[builtins.str] = None,
        custom_key: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
        settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomHostnameSslSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
        wildcard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param certificate_authority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#certificate_authority CustomHostname#certificate_authority}.
        :param custom_certificate: If a custom uploaded certificate is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_certificate CustomHostname#custom_certificate}
        :param custom_key: The key for a custom uploaded certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_key CustomHostname#custom_key}
        :param method: Domain control validation (DCV) method used for this hostname. Available values: ``http``, ``txt``, ``email``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#method CustomHostname#method}
        :param settings: settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#settings CustomHostname#settings}
        :param type: Level of validation to be used for this hostname. Available values: ``dv``. Defaults to ``dv``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#type CustomHostname#type}
        :param wildcard: Indicates whether the certificate covers a wildcard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#wildcard CustomHostname#wildcard}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc12e44f1709e7306d76aaf1846782a7280b06d4803bc4a6014452681f512800)
            check_type(argname="argument certificate_authority", value=certificate_authority, expected_type=type_hints["certificate_authority"])
            check_type(argname="argument custom_certificate", value=custom_certificate, expected_type=type_hints["custom_certificate"])
            check_type(argname="argument custom_key", value=custom_key, expected_type=type_hints["custom_key"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument wildcard", value=wildcard, expected_type=type_hints["wildcard"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_authority is not None:
            self._values["certificate_authority"] = certificate_authority
        if custom_certificate is not None:
            self._values["custom_certificate"] = custom_certificate
        if custom_key is not None:
            self._values["custom_key"] = custom_key
        if method is not None:
            self._values["method"] = method
        if settings is not None:
            self._values["settings"] = settings
        if type is not None:
            self._values["type"] = type
        if wildcard is not None:
            self._values["wildcard"] = wildcard

    @builtins.property
    def certificate_authority(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#certificate_authority CustomHostname#certificate_authority}.'''
        result = self._values.get("certificate_authority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_certificate(self) -> typing.Optional[builtins.str]:
        '''If a custom uploaded certificate is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_certificate CustomHostname#custom_certificate}
        '''
        result = self._values.get("custom_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_key(self) -> typing.Optional[builtins.str]:
        '''The key for a custom uploaded certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#custom_key CustomHostname#custom_key}
        '''
        result = self._values.get("custom_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Domain control validation (DCV) method used for this hostname. Available values: ``http``, ``txt``, ``email``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#method CustomHostname#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomHostnameSslSettings"]]]:
        '''settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#settings CustomHostname#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomHostnameSslSettings"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Level of validation to be used for this hostname. Available values: ``dv``. Defaults to ``dv``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#type CustomHostname#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wildcard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the certificate covers a wildcard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#wildcard CustomHostname#wildcard}
        '''
        result = self._values.get("wildcard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomHostnameSsl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomHostnameSslList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ed6bbd3755b169c1dcd9490a5b10b0016e3fe546cad2c165ddb2e20337f61e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CustomHostnameSslOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a11822dc82160c0b0a24c178d3a0eaf5c9e78c9c8c44d54a486a235097977e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomHostnameSslOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce34c75d92edd0d30d33639980816e87b60c6ca4c77d727acbaa20f6d152d88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c657bf9e0dd8e53c2a9cdf5b2d5991fe945bc275a7f64df6e5b11eca64dbe911)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4122e97283f0e0943126c1e7b388fff06678e1f602d4e240c4641a6aa5f813b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomHostnameSsl]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomHostnameSsl]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomHostnameSsl]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea403eff7e0f3d657667d4baf6086ccc444226d565d17dca5682f2c8806e7819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CustomHostnameSslOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__663b21926d1a54503d78b2d4f735c9aca12fdb5ae279b330f54b2c392771d9ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomHostnameSslSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702794bd60c86bd109c184af1ad7929f23ec85eda26099781301e58934bfee51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="resetCertificateAuthority")
    def reset_certificate_authority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateAuthority", []))

    @jsii.member(jsii_name="resetCustomCertificate")
    def reset_custom_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCertificate", []))

    @jsii.member(jsii_name="resetCustomKey")
    def reset_custom_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomKey", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetWildcard")
    def reset_wildcard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWildcard", []))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "CustomHostnameSslSettingsList":
        return typing.cast("CustomHostnameSslSettingsList", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="validationErrors")
    def validation_errors(self) -> "CustomHostnameSslValidationErrorsList":
        return typing.cast("CustomHostnameSslValidationErrorsList", jsii.get(self, "validationErrors"))

    @builtins.property
    @jsii.member(jsii_name="validationRecords")
    def validation_records(self) -> "CustomHostnameSslValidationRecordsList":
        return typing.cast("CustomHostnameSslValidationRecordsList", jsii.get(self, "validationRecords"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityInput")
    def certificate_authority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateAuthorityInput"))

    @builtins.property
    @jsii.member(jsii_name="customCertificateInput")
    def custom_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="customKeyInput")
    def custom_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomHostnameSslSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomHostnameSslSettings"]]], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="wildcardInput")
    def wildcard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "wildcardInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthority")
    def certificate_authority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthority"))

    @certificate_authority.setter
    def certificate_authority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9779f8b0329e88dbfb19f33d0d45829d723e93f3f5ade778d27ac6b08e81a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthority", value)

    @builtins.property
    @jsii.member(jsii_name="customCertificate")
    def custom_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customCertificate"))

    @custom_certificate.setter
    def custom_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab006b228066d0af31787afa383737ad92ddaf689224e83b46712c043778f675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCertificate", value)

    @builtins.property
    @jsii.member(jsii_name="customKey")
    def custom_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customKey"))

    @custom_key.setter
    def custom_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a17f48c8383f7951c15a68c937b4eeb9aaf84fa5bfd982844b43fccdaebad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customKey", value)

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e2de89b77607e5aff34672908dcb182073e6fe3c4fa61ade9555ecfb70f544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c0d2d525d3d1cc7fa385eb5eb440e702571958440dd7ee017cb0e947b7ace5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="wildcard")
    def wildcard(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wildcard"))

    @wildcard.setter
    def wildcard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d358764a9cd67efbaf1964f84aae15a5a4a8672b5e69832e8fcbc23a96def96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wildcard", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CustomHostnameSsl, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CustomHostnameSsl, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CustomHostnameSsl, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb007a5472eef671f96f7a063117b5b43385031e8f8e37fb07c59c7d4ed78003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslSettings",
    jsii_struct_bases=[],
    name_mapping={
        "ciphers": "ciphers",
        "early_hints": "earlyHints",
        "http2": "http2",
        "min_tls_version": "minTlsVersion",
        "tls13": "tls13",
    },
)
class CustomHostnameSslSettings:
    def __init__(
        self,
        *,
        ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
        early_hints: typing.Optional[builtins.str] = None,
        http2: typing.Optional[builtins.str] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        tls13: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ciphers: List of SSL/TLS ciphers to associate with this certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#ciphers CustomHostname#ciphers}
        :param early_hints: Whether early hints should be supported. Available values: ``on``, ``off``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#early_hints CustomHostname#early_hints}
        :param http2: Whether HTTP2 should be supported. Available values: ``on``, ``off``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#http2 CustomHostname#http2}
        :param min_tls_version: Lowest version of TLS this certificate should support. Available values: ``1.0``, ``1.1``, ``1.2``, ``1.3``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#min_tls_version CustomHostname#min_tls_version}
        :param tls13: Whether TLSv1.3 should be supported. Available values: ``on``, ``off``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#tls13 CustomHostname#tls13}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593a8a11482b32c6ed97b27a2b618398ef4cb94d84bb4979aadeda397ee3e340)
            check_type(argname="argument ciphers", value=ciphers, expected_type=type_hints["ciphers"])
            check_type(argname="argument early_hints", value=early_hints, expected_type=type_hints["early_hints"])
            check_type(argname="argument http2", value=http2, expected_type=type_hints["http2"])
            check_type(argname="argument min_tls_version", value=min_tls_version, expected_type=type_hints["min_tls_version"])
            check_type(argname="argument tls13", value=tls13, expected_type=type_hints["tls13"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ciphers is not None:
            self._values["ciphers"] = ciphers
        if early_hints is not None:
            self._values["early_hints"] = early_hints
        if http2 is not None:
            self._values["http2"] = http2
        if min_tls_version is not None:
            self._values["min_tls_version"] = min_tls_version
        if tls13 is not None:
            self._values["tls13"] = tls13

    @builtins.property
    def ciphers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of SSL/TLS ciphers to associate with this certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#ciphers CustomHostname#ciphers}
        '''
        result = self._values.get("ciphers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def early_hints(self) -> typing.Optional[builtins.str]:
        '''Whether early hints should be supported. Available values: ``on``, ``off``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#early_hints CustomHostname#early_hints}
        '''
        result = self._values.get("early_hints")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http2(self) -> typing.Optional[builtins.str]:
        '''Whether HTTP2 should be supported. Available values: ``on``, ``off``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#http2 CustomHostname#http2}
        '''
        result = self._values.get("http2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_tls_version(self) -> typing.Optional[builtins.str]:
        '''Lowest version of TLS this certificate should support. Available values: ``1.0``, ``1.1``, ``1.2``, ``1.3``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#min_tls_version CustomHostname#min_tls_version}
        '''
        result = self._values.get("min_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls13(self) -> typing.Optional[builtins.str]:
        '''Whether TLSv1.3 should be supported. Available values: ``on``, ``off``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/custom_hostname#tls13 CustomHostname#tls13}
        '''
        result = self._values.get("tls13")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomHostnameSslSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomHostnameSslSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa6cc8285677dd2227b3d615c1821021817bb2303c00c9e85b49996a3ce799ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CustomHostnameSslSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f71202194aae6b5c3033e888229e3e9605decf65db9e1d2728fae9f4dccb6bd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomHostnameSslSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24abfbbbdcdfaa5f6708a8294e68bc924e23252f567edc69fcd745098f08439)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b0733589d356823bb475281912745350205abbaa6bc8f5b6ac8171f4dccf1ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78af2a0a831bc78f1eed964e5e51884980a022be35736e53af2ed276dbb7c4d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomHostnameSslSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomHostnameSslSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomHostnameSslSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58f79c437a3a7ef707cc05ff4b657520151f6b35ea5387aada769ce8f7e0654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CustomHostnameSslSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b01769ef59599079079f042d71ac2bd8391552e42f94a42dce9e11b0be6323a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCiphers")
    def reset_ciphers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiphers", []))

    @jsii.member(jsii_name="resetEarlyHints")
    def reset_early_hints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEarlyHints", []))

    @jsii.member(jsii_name="resetHttp2")
    def reset_http2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2", []))

    @jsii.member(jsii_name="resetMinTlsVersion")
    def reset_min_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTlsVersion", []))

    @jsii.member(jsii_name="resetTls13")
    def reset_tls13(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls13", []))

    @builtins.property
    @jsii.member(jsii_name="ciphersInput")
    def ciphers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ciphersInput"))

    @builtins.property
    @jsii.member(jsii_name="earlyHintsInput")
    def early_hints_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "earlyHintsInput"))

    @builtins.property
    @jsii.member(jsii_name="http2Input")
    def http2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "http2Input"))

    @builtins.property
    @jsii.member(jsii_name="minTlsVersionInput")
    def min_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tls13Input")
    def tls13_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tls13Input"))

    @builtins.property
    @jsii.member(jsii_name="ciphers")
    def ciphers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ciphers"))

    @ciphers.setter
    def ciphers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6f1f055ef36bd33ce870164d7f3cf0988af48323fb195a99b6f16719b9f66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciphers", value)

    @builtins.property
    @jsii.member(jsii_name="earlyHints")
    def early_hints(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "earlyHints"))

    @early_hints.setter
    def early_hints(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3786b21f012c5d7e829d1969b950eabead5123723dceb873a4cd316b4d491106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "earlyHints", value)

    @builtins.property
    @jsii.member(jsii_name="http2")
    def http2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "http2"))

    @http2.setter
    def http2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec400a996dd35fa39c4c8a51e4caaa9601875aa249b71efa2a83c5ecdbee397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2", value)

    @builtins.property
    @jsii.member(jsii_name="minTlsVersion")
    def min_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minTlsVersion"))

    @min_tls_version.setter
    def min_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8bc1c7e0865fd96dc0bea1da610986cd451220ddede47ae11e343ec47440cb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTlsVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tls13")
    def tls13(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tls13"))

    @tls13.setter
    def tls13(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b858a16170a5e0a792ae9b6ccaf06c6d27c0b35c151b4a507a8f458586a89f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls13", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CustomHostnameSslSettings, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CustomHostnameSslSettings, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CustomHostnameSslSettings, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a52417683c4e3fd49606e70fc485ac37a8ea2b7da535a37a13086c1080a6727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslValidationErrors",
    jsii_struct_bases=[],
    name_mapping={},
)
class CustomHostnameSslValidationErrors:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomHostnameSslValidationErrors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomHostnameSslValidationErrorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslValidationErrorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__284416d25bbacfec137fb54b6662a37a2be830ffa657b13ff31640fe41abd9ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomHostnameSslValidationErrorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fc01a89a4bec71cd26add299d5dbd6dc36d883cf31640d1a2fa49e1c26efbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomHostnameSslValidationErrorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c946ab433e600cf513bf298f345bde7487b49eec688a6714792c815ebbb221f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77091f07e3a6ba3bb62077a4ba381f82a4cb8f895640688c793d5a22a04dbcf9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3de6fb4a969a93e11e85e62a06043de133b5d4ff67c3cafcd55ca764a5911bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class CustomHostnameSslValidationErrorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslValidationErrorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b085dd17e9b7cc0104f6f472d08f7107522baa57f9e8772b1a795ebc2d56b92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomHostnameSslValidationErrors]:
        return typing.cast(typing.Optional[CustomHostnameSslValidationErrors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomHostnameSslValidationErrors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b065f61f0f5816364609f411252ba3c1b311c36d008c46a027459136cf799096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslValidationRecords",
    jsii_struct_bases=[],
    name_mapping={},
)
class CustomHostnameSslValidationRecords:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomHostnameSslValidationRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomHostnameSslValidationRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslValidationRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c58367517fae47001fec27a5487ed4350e049ff9572287a9f1fed6bca1e7eb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomHostnameSslValidationRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7d94bdfc87522ac5a3ee576c33ca3d2e738c5a20181f0feec7d4fa9149c58f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomHostnameSslValidationRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95a644a405dad15624f9fbbfce38bf9086c486c238e3641059aabd78e6c63d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfebe9372a49625e444a033068168166a1a657155dd8fa86bdac2075936fc0b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cdeb73c7dbde49866050eef527b140288e1682c00f35c45bd0984383b8fcb5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class CustomHostnameSslValidationRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.customHostname.CustomHostnameSslValidationRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__186cc2fcda9380d9639b49a48f0d6b3405687e7afdab21db4f067bcc1381abf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cnameName")
    def cname_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cnameName"))

    @builtins.property
    @jsii.member(jsii_name="cnameTarget")
    def cname_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cnameTarget"))

    @builtins.property
    @jsii.member(jsii_name="emails")
    def emails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emails"))

    @builtins.property
    @jsii.member(jsii_name="httpBody")
    def http_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpBody"))

    @builtins.property
    @jsii.member(jsii_name="httpUrl")
    def http_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUrl"))

    @builtins.property
    @jsii.member(jsii_name="txtName")
    def txt_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "txtName"))

    @builtins.property
    @jsii.member(jsii_name="txtValue")
    def txt_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "txtValue"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomHostnameSslValidationRecords]:
        return typing.cast(typing.Optional[CustomHostnameSslValidationRecords], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomHostnameSslValidationRecords],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87a7a9f03ff9820f7c5ab633d271f9a463ac35109d0188705047b944130ef6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CustomHostname",
    "CustomHostnameConfig",
    "CustomHostnameSsl",
    "CustomHostnameSslList",
    "CustomHostnameSslOutputReference",
    "CustomHostnameSslSettings",
    "CustomHostnameSslSettingsList",
    "CustomHostnameSslSettingsOutputReference",
    "CustomHostnameSslValidationErrors",
    "CustomHostnameSslValidationErrorsList",
    "CustomHostnameSslValidationErrorsOutputReference",
    "CustomHostnameSslValidationRecords",
    "CustomHostnameSslValidationRecordsList",
    "CustomHostnameSslValidationRecordsOutputReference",
]

publication.publish()

def _typecheckingstub__2999243784abde236613791702b528a1f4896b54dcf17adba234a389d1841b3d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hostname: builtins.str,
    zone_id: builtins.str,
    custom_metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    custom_origin_server: typing.Optional[builtins.str] = None,
    custom_origin_sni: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ssl: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomHostnameSsl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wait_for_ssl_pending_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__514d078b168b29e240b271bc89ee703186a68c6e59c20e8286f3dd99c0cbe73d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomHostnameSsl, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de637288db3c09f8cabeb56459d8d32edce0ca73cf35b168a739e59a09c8f11b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02076b152f8b46094262d0027dfc930a81477e4f6a717130f57de2ac269c0a60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec17de835603301487ab088d7c0b1e989e68675fc038ca2dc41f555e5256987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363b224feee645a6e9d647a4835702b51ad748047425bfa39d8ec804c062a95b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623289f22fb0d206aee353a5a4dd281fc2e7791c35363b498d84a98de18f3f19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b9435597feb457896f7afd402b35f240e355b385e30f087afb4c298373500b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f5ec58ac1d08057ceabff7f21b9fe0ead80236bfe3a796dba741f79d7f3777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92de60c9769d9bcda063e9f820f1972e69185c791f003143b549bdc4352855b2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: builtins.str,
    zone_id: builtins.str,
    custom_metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    custom_origin_server: typing.Optional[builtins.str] = None,
    custom_origin_sni: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ssl: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomHostnameSsl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wait_for_ssl_pending_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc12e44f1709e7306d76aaf1846782a7280b06d4803bc4a6014452681f512800(
    *,
    certificate_authority: typing.Optional[builtins.str] = None,
    custom_certificate: typing.Optional[builtins.str] = None,
    custom_key: typing.Optional[builtins.str] = None,
    method: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomHostnameSslSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
    wildcard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed6bbd3755b169c1dcd9490a5b10b0016e3fe546cad2c165ddb2e20337f61e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a11822dc82160c0b0a24c178d3a0eaf5c9e78c9c8c44d54a486a235097977e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce34c75d92edd0d30d33639980816e87b60c6ca4c77d727acbaa20f6d152d88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c657bf9e0dd8e53c2a9cdf5b2d5991fe945bc275a7f64df6e5b11eca64dbe911(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4122e97283f0e0943126c1e7b388fff06678e1f602d4e240c4641a6aa5f813b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea403eff7e0f3d657667d4baf6086ccc444226d565d17dca5682f2c8806e7819(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomHostnameSsl]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663b21926d1a54503d78b2d4f735c9aca12fdb5ae279b330f54b2c392771d9ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702794bd60c86bd109c184af1ad7929f23ec85eda26099781301e58934bfee51(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomHostnameSslSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9779f8b0329e88dbfb19f33d0d45829d723e93f3f5ade778d27ac6b08e81a1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab006b228066d0af31787afa383737ad92ddaf689224e83b46712c043778f675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a17f48c8383f7951c15a68c937b4eeb9aaf84fa5bfd982844b43fccdaebad2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e2de89b77607e5aff34672908dcb182073e6fe3c4fa61ade9555ecfb70f544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c0d2d525d3d1cc7fa385eb5eb440e702571958440dd7ee017cb0e947b7ace5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d358764a9cd67efbaf1964f84aae15a5a4a8672b5e69832e8fcbc23a96def96(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb007a5472eef671f96f7a063117b5b43385031e8f8e37fb07c59c7d4ed78003(
    value: typing.Optional[typing.Union[CustomHostnameSsl, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593a8a11482b32c6ed97b27a2b618398ef4cb94d84bb4979aadeda397ee3e340(
    *,
    ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
    early_hints: typing.Optional[builtins.str] = None,
    http2: typing.Optional[builtins.str] = None,
    min_tls_version: typing.Optional[builtins.str] = None,
    tls13: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6cc8285677dd2227b3d615c1821021817bb2303c00c9e85b49996a3ce799ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f71202194aae6b5c3033e888229e3e9605decf65db9e1d2728fae9f4dccb6bd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24abfbbbdcdfaa5f6708a8294e68bc924e23252f567edc69fcd745098f08439(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0733589d356823bb475281912745350205abbaa6bc8f5b6ac8171f4dccf1ea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78af2a0a831bc78f1eed964e5e51884980a022be35736e53af2ed276dbb7c4d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58f79c437a3a7ef707cc05ff4b657520151f6b35ea5387aada769ce8f7e0654(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomHostnameSslSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b01769ef59599079079f042d71ac2bd8391552e42f94a42dce9e11b0be6323a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6f1f055ef36bd33ce870164d7f3cf0988af48323fb195a99b6f16719b9f66d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3786b21f012c5d7e829d1969b950eabead5123723dceb873a4cd316b4d491106(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec400a996dd35fa39c4c8a51e4caaa9601875aa249b71efa2a83c5ecdbee397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8bc1c7e0865fd96dc0bea1da610986cd451220ddede47ae11e343ec47440cb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b858a16170a5e0a792ae9b6ccaf06c6d27c0b35c151b4a507a8f458586a89f66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a52417683c4e3fd49606e70fc485ac37a8ea2b7da535a37a13086c1080a6727(
    value: typing.Optional[typing.Union[CustomHostnameSslSettings, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284416d25bbacfec137fb54b6662a37a2be830ffa657b13ff31640fe41abd9ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fc01a89a4bec71cd26add299d5dbd6dc36d883cf31640d1a2fa49e1c26efbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c946ab433e600cf513bf298f345bde7487b49eec688a6714792c815ebbb221f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77091f07e3a6ba3bb62077a4ba381f82a4cb8f895640688c793d5a22a04dbcf9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de6fb4a969a93e11e85e62a06043de133b5d4ff67c3cafcd55ca764a5911bed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b085dd17e9b7cc0104f6f472d08f7107522baa57f9e8772b1a795ebc2d56b92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b065f61f0f5816364609f411252ba3c1b311c36d008c46a027459136cf799096(
    value: typing.Optional[CustomHostnameSslValidationErrors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c58367517fae47001fec27a5487ed4350e049ff9572287a9f1fed6bca1e7eb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7d94bdfc87522ac5a3ee576c33ca3d2e738c5a20181f0feec7d4fa9149c58f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95a644a405dad15624f9fbbfce38bf9086c486c238e3641059aabd78e6c63d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfebe9372a49625e444a033068168166a1a657155dd8fa86bdac2075936fc0b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdeb73c7dbde49866050eef527b140288e1682c00f35c45bd0984383b8fcb5c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186cc2fcda9380d9639b49a48f0d6b3405687e7afdab21db4f067bcc1381abf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87a7a9f03ff9820f7c5ab633d271f9a463ac35109d0188705047b944130ef6b(
    value: typing.Optional[CustomHostnameSslValidationRecords],
) -> None:
    """Type checking stubs"""
    pass
