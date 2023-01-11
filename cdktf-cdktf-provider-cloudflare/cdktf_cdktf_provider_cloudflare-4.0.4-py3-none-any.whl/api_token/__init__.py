'''
# `cloudflare_api_token`

Refer to the Terraform Registory for docs: [`cloudflare_api_token`](https://www.terraform.io/docs/providers/cloudflare/r/api_token).
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


class ApiToken(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiToken",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token cloudflare_api_token}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiTokenPolicy", typing.Dict[builtins.str, typing.Any]]]],
        condition: typing.Optional[typing.Union["ApiTokenCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        expires_on: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        not_before: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token cloudflare_api_token} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the API Token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#name ApiToken#name}
        :param policy: policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#policy ApiToken#policy}
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#condition ApiToken#condition}
        :param expires_on: The expiration time on or after which the token MUST NOT be accepted for processing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#expires_on ApiToken#expires_on}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#id ApiToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param not_before: The time before which the token MUST NOT be accepted for processing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#not_before ApiToken#not_before}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a5e6704427ad2fe30b7889534d44482e7f21fea76b9d8cde11c7caf7d5f114)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiTokenConfig(
            name=name,
            policy=policy,
            condition=condition,
            expires_on=expires_on,
            id=id,
            not_before=not_before,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        request_ip: typing.Optional[typing.Union["ApiTokenConditionRequestIp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param request_ip: request_ip block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#request_ip ApiToken#request_ip}
        '''
        value = ApiTokenCondition(request_ip=request_ip)

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putPolicy")
    def put_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiTokenPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb427a52957161eaaf250b6d2f28b308209eb0b5ebc69cad7e45d219addfe3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicy", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetExpiresOn")
    def reset_expires_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiresOn", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotBefore")
    def reset_not_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotBefore", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> "ApiTokenConditionOutputReference":
        return typing.cast("ApiTokenConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="issuedOn")
    def issued_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuedOn"))

    @builtins.property
    @jsii.member(jsii_name="modifiedOn")
    def modified_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> "ApiTokenPolicyList":
        return typing.cast("ApiTokenPolicyList", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional["ApiTokenCondition"]:
        return typing.cast(typing.Optional["ApiTokenCondition"], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="expiresOnInput")
    def expires_on_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expiresOnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notBeforeInput")
    def not_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiTokenPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiTokenPolicy"]]], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="expiresOn")
    def expires_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresOn"))

    @expires_on.setter
    def expires_on(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7927da8d3b84786c20dbc811de375891e0b7be0ace902af053bd612a032eeff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiresOn", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646c00c137df5778a1a2b0dac3b3654da4f31a440307c6a4d6d1d3a1e95a69ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d54f5d7cd755b0c2b16c3669654384aa691e579ecc28b08bd6d2016ccfdd61d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="notBefore")
    def not_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notBefore"))

    @not_before.setter
    def not_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b110065008918771bc79cec330da0666d7dfe68e63e4ea1045c0976729b54350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notBefore", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiTokenCondition",
    jsii_struct_bases=[],
    name_mapping={"request_ip": "requestIp"},
)
class ApiTokenCondition:
    def __init__(
        self,
        *,
        request_ip: typing.Optional[typing.Union["ApiTokenConditionRequestIp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param request_ip: request_ip block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#request_ip ApiToken#request_ip}
        '''
        if isinstance(request_ip, dict):
            request_ip = ApiTokenConditionRequestIp(**request_ip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65dc574afd1c6f1b89f26db96f983296146c9d83c038be305badc95bf819a1ca)
            check_type(argname="argument request_ip", value=request_ip, expected_type=type_hints["request_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_ip is not None:
            self._values["request_ip"] = request_ip

    @builtins.property
    def request_ip(self) -> typing.Optional["ApiTokenConditionRequestIp"]:
        '''request_ip block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#request_ip ApiToken#request_ip}
        '''
        result = self._values.get("request_ip")
        return typing.cast(typing.Optional["ApiTokenConditionRequestIp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiTokenCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiTokenConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiTokenConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa2810367dcd235bf75255da733f1b3b049cb0a9aad4e0d5012df279a455cc1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestIp")
    def put_request_ip(
        self,
        *,
        in_: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_in: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param in_: List of IP addresses or CIDR notation where the token may be used from. If not specified, the token will be valid for all IP addresses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#in ApiToken#in}
        :param not_in: List of IP addresses or CIDR notation where the token should not be used from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#not_in ApiToken#not_in}
        '''
        value = ApiTokenConditionRequestIp(in_=in_, not_in=not_in)

        return typing.cast(None, jsii.invoke(self, "putRequestIp", [value]))

    @jsii.member(jsii_name="resetRequestIp")
    def reset_request_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestIp", []))

    @builtins.property
    @jsii.member(jsii_name="requestIp")
    def request_ip(self) -> "ApiTokenConditionRequestIpOutputReference":
        return typing.cast("ApiTokenConditionRequestIpOutputReference", jsii.get(self, "requestIp"))

    @builtins.property
    @jsii.member(jsii_name="requestIpInput")
    def request_ip_input(self) -> typing.Optional["ApiTokenConditionRequestIp"]:
        return typing.cast(typing.Optional["ApiTokenConditionRequestIp"], jsii.get(self, "requestIpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiTokenCondition]:
        return typing.cast(typing.Optional[ApiTokenCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiTokenCondition]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2a16249e66bd52074ecbd021001ccd745e65c888d206b63a8971d99bd5140c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiTokenConditionRequestIp",
    jsii_struct_bases=[],
    name_mapping={"in_": "in", "not_in": "notIn"},
)
class ApiTokenConditionRequestIp:
    def __init__(
        self,
        *,
        in_: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_in: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param in_: List of IP addresses or CIDR notation where the token may be used from. If not specified, the token will be valid for all IP addresses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#in ApiToken#in}
        :param not_in: List of IP addresses or CIDR notation where the token should not be used from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#not_in ApiToken#not_in}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12dfe21973f1da4f7a037b9049eba885fa3c760bc9850267f5f6467de61afd22)
            check_type(argname="argument in_", value=in_, expected_type=type_hints["in_"])
            check_type(argname="argument not_in", value=not_in, expected_type=type_hints["not_in"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if in_ is not None:
            self._values["in_"] = in_
        if not_in is not None:
            self._values["not_in"] = not_in

    @builtins.property
    def in_(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IP addresses or CIDR notation where the token may be used from.

        If not specified, the token will be valid for all IP addresses.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#in ApiToken#in}
        '''
        result = self._values.get("in_")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_in(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IP addresses or CIDR notation where the token should not be used from.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#not_in ApiToken#not_in}
        '''
        result = self._values.get("not_in")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiTokenConditionRequestIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiTokenConditionRequestIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiTokenConditionRequestIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c49d6f15c31848d722456e976ddef010c17742000f0442d473063208eb0aad0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIn")
    def reset_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIn", []))

    @jsii.member(jsii_name="resetNotIn")
    def reset_not_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotIn", []))

    @builtins.property
    @jsii.member(jsii_name="inInput")
    def in_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inInput"))

    @builtins.property
    @jsii.member(jsii_name="notInInput")
    def not_in_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notInInput"))

    @builtins.property
    @jsii.member(jsii_name="in")
    def in_(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "in"))

    @in_.setter
    def in_(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a352b1e5878ba540c11786517d0b4a2e72161e8ef7b7a2b7fdce75711cb69b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "in", value)

    @builtins.property
    @jsii.member(jsii_name="notIn")
    def not_in(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notIn"))

    @not_in.setter
    def not_in(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e829ee6656e65a20e53c3c2cdb45d2de8a42d5e14d991865e8ff0d42609faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notIn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiTokenConditionRequestIp]:
        return typing.cast(typing.Optional[ApiTokenConditionRequestIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiTokenConditionRequestIp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4e702dcf78845e29817c715318850fa5eb9ffdb2354ac07853c22fd8aef2df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiTokenConfig",
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
        "policy": "policy",
        "condition": "condition",
        "expires_on": "expiresOn",
        "id": "id",
        "not_before": "notBefore",
    },
)
class ApiTokenConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiTokenPolicy", typing.Dict[builtins.str, typing.Any]]]],
        condition: typing.Optional[typing.Union[ApiTokenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        expires_on: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        not_before: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the API Token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#name ApiToken#name}
        :param policy: policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#policy ApiToken#policy}
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#condition ApiToken#condition}
        :param expires_on: The expiration time on or after which the token MUST NOT be accepted for processing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#expires_on ApiToken#expires_on}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#id ApiToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param not_before: The time before which the token MUST NOT be accepted for processing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#not_before ApiToken#not_before}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition, dict):
            condition = ApiTokenCondition(**condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb17924e77f6d73c5eaecca8fb2c9a9e50c5dd1fb30471673618875aff36d790)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument expires_on", value=expires_on, expected_type=type_hints["expires_on"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument not_before", value=not_before, expected_type=type_hints["not_before"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy": policy,
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
        if condition is not None:
            self._values["condition"] = condition
        if expires_on is not None:
            self._values["expires_on"] = expires_on
        if id is not None:
            self._values["id"] = id
        if not_before is not None:
            self._values["not_before"] = not_before

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
        '''Name of the API Token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#name ApiToken#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiTokenPolicy"]]:
        '''policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#policy ApiToken#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiTokenPolicy"]], result)

    @builtins.property
    def condition(self) -> typing.Optional[ApiTokenCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#condition ApiToken#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[ApiTokenCondition], result)

    @builtins.property
    def expires_on(self) -> typing.Optional[builtins.str]:
        '''The expiration time on or after which the token MUST NOT be accepted for processing.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#expires_on ApiToken#expires_on}
        '''
        result = self._values.get("expires_on")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#id ApiToken#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def not_before(self) -> typing.Optional[builtins.str]:
        '''The time before which the token MUST NOT be accepted for processing.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#not_before ApiToken#not_before}
        '''
        result = self._values.get("not_before")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiTokenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiTokenPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "permission_groups": "permissionGroups",
        "resources": "resources",
        "effect": "effect",
    },
)
class ApiTokenPolicy:
    def __init__(
        self,
        *,
        permission_groups: typing.Sequence[builtins.str],
        resources: typing.Mapping[builtins.str, builtins.str],
        effect: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param permission_groups: List of permissions groups IDs. See `documentation <https://developers.cloudflare.com/api/tokens/create/permissions>`_ for more information. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#permission_groups ApiToken#permission_groups}
        :param resources: Describes what operations against which resources are allowed or denied. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#resources ApiToken#resources}
        :param effect: Effect of the policy. Available values: ``allow``, ``deny``. Defaults to ``allow``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#effect ApiToken#effect}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d691ab973cf89d8f7ddddaf7a2f9bafe16f9d712917122e444b591477a37b0e)
            check_type(argname="argument permission_groups", value=permission_groups, expected_type=type_hints["permission_groups"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permission_groups": permission_groups,
            "resources": resources,
        }
        if effect is not None:
            self._values["effect"] = effect

    @builtins.property
    def permission_groups(self) -> typing.List[builtins.str]:
        '''List of permissions groups IDs. See `documentation <https://developers.cloudflare.com/api/tokens/create/permissions>`_ for more information.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#permission_groups ApiToken#permission_groups}
        '''
        result = self._values.get("permission_groups")
        assert result is not None, "Required property 'permission_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Describes what operations against which resources are allowed or denied.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#resources ApiToken#resources}
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def effect(self) -> typing.Optional[builtins.str]:
        '''Effect of the policy. Available values: ``allow``, ``deny``. Defaults to ``allow``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/api_token#effect ApiToken#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiTokenPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiTokenPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiTokenPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec2a461739d4097b332e2481a1733589b09ef0b3badfad0a6d3df68e890eaa48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApiTokenPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1890e24b162a3f2da40b887f3ff1d724fe47287f29da2eff7114446f3e0b3881)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiTokenPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6e622bcae469d29646d3139524d73711b211ed417370831c99c34b2f0a93db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ede4052154da2b0322b3b97d38caa9369ebd3c478f93f306b762ce9305027ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33dac36daa3186fb55c7676500b3a870a770b165ca3f8dc4d830c4f4d02ce5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiTokenPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiTokenPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiTokenPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8c297571312dac508ece6043f8980af5a2558398e1e72a97aefc34c26c2885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ApiTokenPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.apiToken.ApiTokenPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e90a723bf6400954f7aa0f911f136b072376eb2adc2028703a814b6d64391f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEffect")
    def reset_effect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffect", []))

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionGroupsInput")
    def permission_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permissionGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9900ca2b088042c2d4d4fef72d1f8511005a0df9d7ea1ef305c3c743ff6ea21b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value)

    @builtins.property
    @jsii.member(jsii_name="permissionGroups")
    def permission_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permissionGroups"))

    @permission_groups.setter
    def permission_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c275eacb1da6b5c5929d14c486d0278703744a41a466f99a10b72d838e0ad262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionGroups", value)

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00492f83ca8e5584097f8b82b5dded40bdb4b1e8cde0e6e6d94584d3ffd1288b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ApiTokenPolicy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ApiTokenPolicy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ApiTokenPolicy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3846c4c6f3690dd217db2db9b9d6105bda1aa8b89e6863bfc85226b1e49d3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ApiToken",
    "ApiTokenCondition",
    "ApiTokenConditionOutputReference",
    "ApiTokenConditionRequestIp",
    "ApiTokenConditionRequestIpOutputReference",
    "ApiTokenConfig",
    "ApiTokenPolicy",
    "ApiTokenPolicyList",
    "ApiTokenPolicyOutputReference",
]

publication.publish()

def _typecheckingstub__f5a5e6704427ad2fe30b7889534d44482e7f21fea76b9d8cde11c7caf7d5f114(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiTokenPolicy, typing.Dict[builtins.str, typing.Any]]]],
    condition: typing.Optional[typing.Union[ApiTokenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    expires_on: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    not_before: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8eb427a52957161eaaf250b6d2f28b308209eb0b5ebc69cad7e45d219addfe3f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiTokenPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7927da8d3b84786c20dbc811de375891e0b7be0ace902af053bd612a032eeff1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646c00c137df5778a1a2b0dac3b3654da4f31a440307c6a4d6d1d3a1e95a69ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d54f5d7cd755b0c2b16c3669654384aa691e579ecc28b08bd6d2016ccfdd61d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b110065008918771bc79cec330da0666d7dfe68e63e4ea1045c0976729b54350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65dc574afd1c6f1b89f26db96f983296146c9d83c038be305badc95bf819a1ca(
    *,
    request_ip: typing.Optional[typing.Union[ApiTokenConditionRequestIp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2810367dcd235bf75255da733f1b3b049cb0a9aad4e0d5012df279a455cc1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2a16249e66bd52074ecbd021001ccd745e65c888d206b63a8971d99bd5140c(
    value: typing.Optional[ApiTokenCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12dfe21973f1da4f7a037b9049eba885fa3c760bc9850267f5f6467de61afd22(
    *,
    in_: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_in: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c49d6f15c31848d722456e976ddef010c17742000f0442d473063208eb0aad0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a352b1e5878ba540c11786517d0b4a2e72161e8ef7b7a2b7fdce75711cb69b77(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e829ee6656e65a20e53c3c2cdb45d2de8a42d5e14d991865e8ff0d42609faf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4e702dcf78845e29817c715318850fa5eb9ffdb2354ac07853c22fd8aef2df(
    value: typing.Optional[ApiTokenConditionRequestIp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb17924e77f6d73c5eaecca8fb2c9a9e50c5dd1fb30471673618875aff36d790(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiTokenPolicy, typing.Dict[builtins.str, typing.Any]]]],
    condition: typing.Optional[typing.Union[ApiTokenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    expires_on: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    not_before: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d691ab973cf89d8f7ddddaf7a2f9bafe16f9d712917122e444b591477a37b0e(
    *,
    permission_groups: typing.Sequence[builtins.str],
    resources: typing.Mapping[builtins.str, builtins.str],
    effect: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2a461739d4097b332e2481a1733589b09ef0b3badfad0a6d3df68e890eaa48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1890e24b162a3f2da40b887f3ff1d724fe47287f29da2eff7114446f3e0b3881(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6e622bcae469d29646d3139524d73711b211ed417370831c99c34b2f0a93db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ede4052154da2b0322b3b97d38caa9369ebd3c478f93f306b762ce9305027ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33dac36daa3186fb55c7676500b3a870a770b165ca3f8dc4d830c4f4d02ce5da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8c297571312dac508ece6043f8980af5a2558398e1e72a97aefc34c26c2885(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiTokenPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e90a723bf6400954f7aa0f911f136b072376eb2adc2028703a814b6d64391f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9900ca2b088042c2d4d4fef72d1f8511005a0df9d7ea1ef305c3c743ff6ea21b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c275eacb1da6b5c5929d14c486d0278703744a41a466f99a10b72d838e0ad262(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00492f83ca8e5584097f8b82b5dded40bdb4b1e8cde0e6e6d94584d3ffd1288b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3846c4c6f3690dd217db2db9b9d6105bda1aa8b89e6863bfc85226b1e49d3b4(
    value: typing.Optional[typing.Union[ApiTokenPolicy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
