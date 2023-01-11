'''
# `cloudflare_origin_ca_certificate`

Refer to the Terraform Registory for docs: [`cloudflare_origin_ca_certificate`](https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate).
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


class OriginCaCertificate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.originCaCertificate.OriginCaCertificate",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate cloudflare_origin_ca_certificate}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hostnames: typing.Sequence[builtins.str],
        request_type: builtins.str,
        csr: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        min_days_for_renewal: typing.Optional[jsii.Number] = None,
        requested_validity: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate cloudflare_origin_ca_certificate} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hostnames: A list of hostnames or wildcard names bound to the certificate. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#hostnames OriginCaCertificate#hostnames}
        :param request_type: The signature type desired on the certificate. Available values: ``origin-rsa``, ``origin-ecc``, ``keyless-certificate``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#request_type OriginCaCertificate#request_type}
        :param csr: The Certificate Signing Request. Must be newline-encoded. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#csr OriginCaCertificate#csr}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#id OriginCaCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_days_for_renewal: Number of days prior to the expiry to trigger a renewal of the certificate if a Terraform operation is run. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#min_days_for_renewal OriginCaCertificate#min_days_for_renewal}
        :param requested_validity: The number of days for which the certificate should be valid. Available values: ``7``, ``30``, ``90``, ``365``, ``730``, ``1095``, ``5475``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#requested_validity OriginCaCertificate#requested_validity}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3403a3d31c1f43bff193b22c205d982d6d20230e1bc2886b39f2be46c3d8d0ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OriginCaCertificateConfig(
            hostnames=hostnames,
            request_type=request_type,
            csr=csr,
            id=id,
            min_days_for_renewal=min_days_for_renewal,
            requested_validity=requested_validity,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetCsr")
    def reset_csr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsr", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinDaysForRenewal")
    def reset_min_days_for_renewal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinDaysForRenewal", []))

    @jsii.member(jsii_name="resetRequestedValidity")
    def reset_requested_validity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestedValidity", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="expiresOn")
    def expires_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresOn"))

    @builtins.property
    @jsii.member(jsii_name="csrInput")
    def csr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "csrInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnamesInput")
    def hostnames_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostnamesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minDaysForRenewalInput")
    def min_days_for_renewal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minDaysForRenewalInput"))

    @builtins.property
    @jsii.member(jsii_name="requestedValidityInput")
    def requested_validity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestedValidityInput"))

    @builtins.property
    @jsii.member(jsii_name="requestTypeInput")
    def request_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="csr")
    def csr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "csr"))

    @csr.setter
    def csr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071e419510ee4f2b36592ff3b796d101815091269879943d6de8db50585b6526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "csr", value)

    @builtins.property
    @jsii.member(jsii_name="hostnames")
    def hostnames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostnames"))

    @hostnames.setter
    def hostnames(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d9583cdfd616c9f7060f3e8fdddc95e063d1082077013bff8b870ec1a9cfa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnames", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13eec198e8223a76747830635e4e9cdc1df3240a2b6365028f108f4a761b702e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="minDaysForRenewal")
    def min_days_for_renewal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minDaysForRenewal"))

    @min_days_for_renewal.setter
    def min_days_for_renewal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccce02e63f777895f8ebc003c361fcf4455daaed7f8afba640d7b3d4333fc3bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minDaysForRenewal", value)

    @builtins.property
    @jsii.member(jsii_name="requestedValidity")
    def requested_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requestedValidity"))

    @requested_validity.setter
    def requested_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bca3eb60614e227f2584bc135f02d7a3287b8fd06ce63f049a03e7fe90a42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedValidity", value)

    @builtins.property
    @jsii.member(jsii_name="requestType")
    def request_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestType"))

    @request_type.setter
    def request_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8980a71fd8746afef0bae9e1a208206e816b79748704b75b322c1562170eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.originCaCertificate.OriginCaCertificateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hostnames": "hostnames",
        "request_type": "requestType",
        "csr": "csr",
        "id": "id",
        "min_days_for_renewal": "minDaysForRenewal",
        "requested_validity": "requestedValidity",
    },
)
class OriginCaCertificateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hostnames: typing.Sequence[builtins.str],
        request_type: builtins.str,
        csr: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        min_days_for_renewal: typing.Optional[jsii.Number] = None,
        requested_validity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hostnames: A list of hostnames or wildcard names bound to the certificate. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#hostnames OriginCaCertificate#hostnames}
        :param request_type: The signature type desired on the certificate. Available values: ``origin-rsa``, ``origin-ecc``, ``keyless-certificate``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#request_type OriginCaCertificate#request_type}
        :param csr: The Certificate Signing Request. Must be newline-encoded. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#csr OriginCaCertificate#csr}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#id OriginCaCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_days_for_renewal: Number of days prior to the expiry to trigger a renewal of the certificate if a Terraform operation is run. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#min_days_for_renewal OriginCaCertificate#min_days_for_renewal}
        :param requested_validity: The number of days for which the certificate should be valid. Available values: ``7``, ``30``, ``90``, ``365``, ``730``, ``1095``, ``5475``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#requested_validity OriginCaCertificate#requested_validity}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__674cf4c1587e8f76601c4d76c7def0bc250ff1e5786f54c53a976dcff219ead6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hostnames", value=hostnames, expected_type=type_hints["hostnames"])
            check_type(argname="argument request_type", value=request_type, expected_type=type_hints["request_type"])
            check_type(argname="argument csr", value=csr, expected_type=type_hints["csr"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument min_days_for_renewal", value=min_days_for_renewal, expected_type=type_hints["min_days_for_renewal"])
            check_type(argname="argument requested_validity", value=requested_validity, expected_type=type_hints["requested_validity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostnames": hostnames,
            "request_type": request_type,
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
        if csr is not None:
            self._values["csr"] = csr
        if id is not None:
            self._values["id"] = id
        if min_days_for_renewal is not None:
            self._values["min_days_for_renewal"] = min_days_for_renewal
        if requested_validity is not None:
            self._values["requested_validity"] = requested_validity

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
    def hostnames(self) -> typing.List[builtins.str]:
        '''A list of hostnames or wildcard names bound to the certificate.

        **Modifying this attribute will force creation of a new resource.**

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#hostnames OriginCaCertificate#hostnames}
        '''
        result = self._values.get("hostnames")
        assert result is not None, "Required property 'hostnames' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def request_type(self) -> builtins.str:
        '''The signature type desired on the certificate.

        Available values: ``origin-rsa``, ``origin-ecc``, ``keyless-certificate``. **Modifying this attribute will force creation of a new resource.**

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#request_type OriginCaCertificate#request_type}
        '''
        result = self._values.get("request_type")
        assert result is not None, "Required property 'request_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def csr(self) -> typing.Optional[builtins.str]:
        '''The Certificate Signing Request. Must be newline-encoded. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#csr OriginCaCertificate#csr}
        '''
        result = self._values.get("csr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#id OriginCaCertificate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_days_for_renewal(self) -> typing.Optional[jsii.Number]:
        '''Number of days prior to the expiry to trigger a renewal of the certificate if a Terraform operation is run.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#min_days_for_renewal OriginCaCertificate#min_days_for_renewal}
        '''
        result = self._values.get("min_days_for_renewal")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def requested_validity(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which the certificate should be valid.

        Available values: ``7``, ``30``, ``90``, ``365``, ``730``, ``1095``, ``5475``. **Modifying this attribute will force creation of a new resource.**

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/origin_ca_certificate#requested_validity OriginCaCertificate#requested_validity}
        '''
        result = self._values.get("requested_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginCaCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OriginCaCertificate",
    "OriginCaCertificateConfig",
]

publication.publish()

def _typecheckingstub__3403a3d31c1f43bff193b22c205d982d6d20230e1bc2886b39f2be46c3d8d0ca(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hostnames: typing.Sequence[builtins.str],
    request_type: builtins.str,
    csr: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    min_days_for_renewal: typing.Optional[jsii.Number] = None,
    requested_validity: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__071e419510ee4f2b36592ff3b796d101815091269879943d6de8db50585b6526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d9583cdfd616c9f7060f3e8fdddc95e063d1082077013bff8b870ec1a9cfa9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13eec198e8223a76747830635e4e9cdc1df3240a2b6365028f108f4a761b702e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccce02e63f777895f8ebc003c361fcf4455daaed7f8afba640d7b3d4333fc3bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bca3eb60614e227f2584bc135f02d7a3287b8fd06ce63f049a03e7fe90a42b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8980a71fd8746afef0bae9e1a208206e816b79748704b75b322c1562170eb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674cf4c1587e8f76601c4d76c7def0bc250ff1e5786f54c53a976dcff219ead6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostnames: typing.Sequence[builtins.str],
    request_type: builtins.str,
    csr: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    min_days_for_renewal: typing.Optional[jsii.Number] = None,
    requested_validity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
