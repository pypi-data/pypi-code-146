'''
# `okta_factor_totp`

Refer to the Terraform Registory for docs: [`okta_factor_totp`](https://www.terraform.io/docs/providers/okta/r/factor_totp).
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


class FactorTotp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.factorTotp.FactorTotp",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/factor_totp okta_factor_totp}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        clock_drift_interval: typing.Optional[jsii.Number] = None,
        hmac_algorithm: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        otp_length: typing.Optional[jsii.Number] = None,
        shared_secret_encoding: typing.Optional[builtins.str] = None,
        time_step: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/factor_totp okta_factor_totp} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Factor name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#name FactorTotp#name}
        :param clock_drift_interval: Clock drift interval. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#clock_drift_interval FactorTotp#clock_drift_interval}
        :param hmac_algorithm: Hash-based message authentication code algorithm. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#hmac_algorithm FactorTotp#hmac_algorithm}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#id FactorTotp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param otp_length: Factor name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#otp_length FactorTotp#otp_length}
        :param shared_secret_encoding: Shared secret encoding. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#shared_secret_encoding FactorTotp#shared_secret_encoding}
        :param time_step: Time step in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#time_step FactorTotp#time_step}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4bfc7218b2aafc31f87962912b8e5b11250314c5f4cf280efca8430d1495de0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FactorTotpConfig(
            name=name,
            clock_drift_interval=clock_drift_interval,
            hmac_algorithm=hmac_algorithm,
            id=id,
            otp_length=otp_length,
            shared_secret_encoding=shared_secret_encoding,
            time_step=time_step,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetClockDriftInterval")
    def reset_clock_drift_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClockDriftInterval", []))

    @jsii.member(jsii_name="resetHmacAlgorithm")
    def reset_hmac_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHmacAlgorithm", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOtpLength")
    def reset_otp_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOtpLength", []))

    @jsii.member(jsii_name="resetSharedSecretEncoding")
    def reset_shared_secret_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedSecretEncoding", []))

    @jsii.member(jsii_name="resetTimeStep")
    def reset_time_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeStep", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="clockDriftIntervalInput")
    def clock_drift_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clockDriftIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="hmacAlgorithmInput")
    def hmac_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hmacAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="otpLengthInput")
    def otp_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "otpLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedSecretEncodingInput")
    def shared_secret_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedSecretEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeStepInput")
    def time_step_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeStepInput"))

    @builtins.property
    @jsii.member(jsii_name="clockDriftInterval")
    def clock_drift_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clockDriftInterval"))

    @clock_drift_interval.setter
    def clock_drift_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c43ff01c4892b142f16dc460fc4a13c4aef9b5ce68e9717990a61ec13f1efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clockDriftInterval", value)

    @builtins.property
    @jsii.member(jsii_name="hmacAlgorithm")
    def hmac_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hmacAlgorithm"))

    @hmac_algorithm.setter
    def hmac_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b15c28a22f3db941b9abb1bcd2a76b5a68df398d0c47df341ceac3b3cb197e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hmacAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769362051fb6ce0ebf7640b07bb0045df8a63586304e843f36646c3c2714c1a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea3831cc0d4cc21a456fa29372b2276c549abcd91bf8a886c6fffe9a7c6ea7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="otpLength")
    def otp_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "otpLength"))

    @otp_length.setter
    def otp_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd9fecd3639a33e8ddf7abba8eef906f4fa5d62fe2ea61a3b099e2cf2e80a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "otpLength", value)

    @builtins.property
    @jsii.member(jsii_name="sharedSecretEncoding")
    def shared_secret_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedSecretEncoding"))

    @shared_secret_encoding.setter
    def shared_secret_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c61eb64519f55826cd8e5581e61eed62d9fa1000baabc9b525fe194442f03f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedSecretEncoding", value)

    @builtins.property
    @jsii.member(jsii_name="timeStep")
    def time_step(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeStep"))

    @time_step.setter
    def time_step(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__254062e35651f4da07737450128b3081acb417fd82f99a15e0b6f93d898aad6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeStep", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.factorTotp.FactorTotpConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "clock_drift_interval": "clockDriftInterval",
        "hmac_algorithm": "hmacAlgorithm",
        "id": "id",
        "otp_length": "otpLength",
        "shared_secret_encoding": "sharedSecretEncoding",
        "time_step": "timeStep",
    },
)
class FactorTotpConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        clock_drift_interval: typing.Optional[jsii.Number] = None,
        hmac_algorithm: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        otp_length: typing.Optional[jsii.Number] = None,
        shared_secret_encoding: typing.Optional[builtins.str] = None,
        time_step: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Factor name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#name FactorTotp#name}
        :param clock_drift_interval: Clock drift interval. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#clock_drift_interval FactorTotp#clock_drift_interval}
        :param hmac_algorithm: Hash-based message authentication code algorithm. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#hmac_algorithm FactorTotp#hmac_algorithm}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#id FactorTotp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param otp_length: Factor name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#otp_length FactorTotp#otp_length}
        :param shared_secret_encoding: Shared secret encoding. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#shared_secret_encoding FactorTotp#shared_secret_encoding}
        :param time_step: Time step in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#time_step FactorTotp#time_step}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0562d8a9fe6f6c6e06da27a94d8f7271ac22999a45cb27991d28a7a9c507132)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument clock_drift_interval", value=clock_drift_interval, expected_type=type_hints["clock_drift_interval"])
            check_type(argname="argument hmac_algorithm", value=hmac_algorithm, expected_type=type_hints["hmac_algorithm"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument otp_length", value=otp_length, expected_type=type_hints["otp_length"])
            check_type(argname="argument shared_secret_encoding", value=shared_secret_encoding, expected_type=type_hints["shared_secret_encoding"])
            check_type(argname="argument time_step", value=time_step, expected_type=type_hints["time_step"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if clock_drift_interval is not None:
            self._values["clock_drift_interval"] = clock_drift_interval
        if hmac_algorithm is not None:
            self._values["hmac_algorithm"] = hmac_algorithm
        if id is not None:
            self._values["id"] = id
        if otp_length is not None:
            self._values["otp_length"] = otp_length
        if shared_secret_encoding is not None:
            self._values["shared_secret_encoding"] = shared_secret_encoding
        if time_step is not None:
            self._values["time_step"] = time_step

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
    def name(self) -> builtins.str:
        '''Factor name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#name FactorTotp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def clock_drift_interval(self) -> typing.Optional[jsii.Number]:
        '''Clock drift interval.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#clock_drift_interval FactorTotp#clock_drift_interval}
        '''
        result = self._values.get("clock_drift_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hmac_algorithm(self) -> typing.Optional[builtins.str]:
        '''Hash-based message authentication code algorithm.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#hmac_algorithm FactorTotp#hmac_algorithm}
        '''
        result = self._values.get("hmac_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#id FactorTotp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def otp_length(self) -> typing.Optional[jsii.Number]:
        '''Factor name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#otp_length FactorTotp#otp_length}
        '''
        result = self._values.get("otp_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shared_secret_encoding(self) -> typing.Optional[builtins.str]:
        '''Shared secret encoding.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#shared_secret_encoding FactorTotp#shared_secret_encoding}
        '''
        result = self._values.get("shared_secret_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_step(self) -> typing.Optional[jsii.Number]:
        '''Time step in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/factor_totp#time_step FactorTotp#time_step}
        '''
        result = self._values.get("time_step")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FactorTotpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FactorTotp",
    "FactorTotpConfig",
]

publication.publish()

def _typecheckingstub__e4bfc7218b2aafc31f87962912b8e5b11250314c5f4cf280efca8430d1495de0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    clock_drift_interval: typing.Optional[jsii.Number] = None,
    hmac_algorithm: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    otp_length: typing.Optional[jsii.Number] = None,
    shared_secret_encoding: typing.Optional[builtins.str] = None,
    time_step: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__a5c43ff01c4892b142f16dc460fc4a13c4aef9b5ce68e9717990a61ec13f1efa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b15c28a22f3db941b9abb1bcd2a76b5a68df398d0c47df341ceac3b3cb197e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769362051fb6ce0ebf7640b07bb0045df8a63586304e843f36646c3c2714c1a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea3831cc0d4cc21a456fa29372b2276c549abcd91bf8a886c6fffe9a7c6ea7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd9fecd3639a33e8ddf7abba8eef906f4fa5d62fe2ea61a3b099e2cf2e80a3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61eb64519f55826cd8e5581e61eed62d9fa1000baabc9b525fe194442f03f9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254062e35651f4da07737450128b3081acb417fd82f99a15e0b6f93d898aad6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0562d8a9fe6f6c6e06da27a94d8f7271ac22999a45cb27991d28a7a9c507132(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    clock_drift_interval: typing.Optional[jsii.Number] = None,
    hmac_algorithm: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    otp_length: typing.Optional[jsii.Number] = None,
    shared_secret_encoding: typing.Optional[builtins.str] = None,
    time_step: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
