'''
# `data_aws_servicequotas_service_quota`

Refer to the Terraform Registory for docs: [`data_aws_servicequotas_service_quota`](https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota).
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


class DataAwsServicequotasServiceQuota(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsServicequotasServiceQuota.DataAwsServicequotasServiceQuota",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota aws_servicequotas_service_quota}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        service_code: builtins.str,
        id: typing.Optional[builtins.str] = None,
        quota_code: typing.Optional[builtins.str] = None,
        quota_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota aws_servicequotas_service_quota} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param service_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#service_code DataAwsServicequotasServiceQuota#service_code}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#id DataAwsServicequotasServiceQuota#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param quota_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#quota_code DataAwsServicequotasServiceQuota#quota_code}.
        :param quota_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#quota_name DataAwsServicequotasServiceQuota#quota_name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc42d2be1dbfeb82d7c384962bd143e5d81127bf3cceaa1d4a23a130f308cbe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAwsServicequotasServiceQuotaConfig(
            service_code=service_code,
            id=id,
            quota_code=quota_code,
            quota_name=quota_name,
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

    @jsii.member(jsii_name="resetQuotaCode")
    def reset_quota_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotaCode", []))

    @jsii.member(jsii_name="resetQuotaName")
    def reset_quota_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotaName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="adjustable")
    def adjustable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "adjustable"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="defaultValue")
    def default_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultValue"))

    @builtins.property
    @jsii.member(jsii_name="globalQuota")
    def global_quota(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "globalQuota"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaCodeInput")
    def quota_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quotaCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaNameInput")
    def quota_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quotaNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceCodeInput")
    def service_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b9645cff0f0d0ac5bf72acb167db13913c3dbf03e6264c8d55cfa03d9e0706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="quotaCode")
    def quota_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaCode"))

    @quota_code.setter
    def quota_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85951f7740e1d0888b6c0e985ebb79d01a39fa135a1a7d33b090e14b39bc6179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaCode", value)

    @builtins.property
    @jsii.member(jsii_name="quotaName")
    def quota_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaName"))

    @quota_name.setter
    def quota_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46bfe427101128eb56864f7a7e061dbb7aa72adf2c4c9d038410a05f0dead052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaName", value)

    @builtins.property
    @jsii.member(jsii_name="serviceCode")
    def service_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceCode"))

    @service_code.setter
    def service_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664e56e2cdb2371a76433ff2b0a3b8bcf19758b4db08accc23d45e90bc33e0c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceCode", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsServicequotasServiceQuota.DataAwsServicequotasServiceQuotaConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "service_code": "serviceCode",
        "id": "id",
        "quota_code": "quotaCode",
        "quota_name": "quotaName",
    },
)
class DataAwsServicequotasServiceQuotaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        service_code: builtins.str,
        id: typing.Optional[builtins.str] = None,
        quota_code: typing.Optional[builtins.str] = None,
        quota_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param service_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#service_code DataAwsServicequotasServiceQuota#service_code}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#id DataAwsServicequotasServiceQuota#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param quota_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#quota_code DataAwsServicequotasServiceQuota#quota_code}.
        :param quota_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#quota_name DataAwsServicequotasServiceQuota#quota_name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d603fb1ece57d056352c6ac304fd967565c3c7ac7cfa76f667d6a7b38519b5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument service_code", value=service_code, expected_type=type_hints["service_code"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument quota_code", value=quota_code, expected_type=type_hints["quota_code"])
            check_type(argname="argument quota_name", value=quota_name, expected_type=type_hints["quota_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_code": service_code,
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
        if quota_code is not None:
            self._values["quota_code"] = quota_code
        if quota_name is not None:
            self._values["quota_name"] = quota_name

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
    def service_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#service_code DataAwsServicequotasServiceQuota#service_code}.'''
        result = self._values.get("service_code")
        assert result is not None, "Required property 'service_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#id DataAwsServicequotasServiceQuota#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#quota_code DataAwsServicequotasServiceQuota#quota_code}.'''
        result = self._values.get("quota_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/servicequotas_service_quota#quota_name DataAwsServicequotasServiceQuota#quota_name}.'''
        result = self._values.get("quota_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsServicequotasServiceQuotaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataAwsServicequotasServiceQuota",
    "DataAwsServicequotasServiceQuotaConfig",
]

publication.publish()

def _typecheckingstub__bcc42d2be1dbfeb82d7c384962bd143e5d81127bf3cceaa1d4a23a130f308cbe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    service_code: builtins.str,
    id: typing.Optional[builtins.str] = None,
    quota_code: typing.Optional[builtins.str] = None,
    quota_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__28b9645cff0f0d0ac5bf72acb167db13913c3dbf03e6264c8d55cfa03d9e0706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85951f7740e1d0888b6c0e985ebb79d01a39fa135a1a7d33b090e14b39bc6179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46bfe427101128eb56864f7a7e061dbb7aa72adf2c4c9d038410a05f0dead052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664e56e2cdb2371a76433ff2b0a3b8bcf19758b4db08accc23d45e90bc33e0c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d603fb1ece57d056352c6ac304fd967565c3c7ac7cfa76f667d6a7b38519b5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_code: builtins.str,
    id: typing.Optional[builtins.str] = None,
    quota_code: typing.Optional[builtins.str] = None,
    quota_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
