'''
# `cloudflare_load_balancer_monitor`

Refer to the Terraform Registory for docs: [`cloudflare_load_balancer_monitor`](https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor).
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


class LoadBalancerMonitor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerMonitor.LoadBalancerMonitor",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor cloudflare_load_balancer_monitor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: typing.Optional[builtins.str] = None,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        expected_body: typing.Optional[builtins.str] = None,
        expected_codes: typing.Optional[builtins.str] = None,
        follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerMonitorHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        probe_zone: typing.Optional[builtins.str] = None,
        retries: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor cloudflare_load_balancer_monitor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#account_id LoadBalancerMonitor#account_id}
        :param allow_insecure: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#allow_insecure LoadBalancerMonitor#allow_insecure}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#description LoadBalancerMonitor#description}.
        :param expected_body: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#expected_body LoadBalancerMonitor#expected_body}.
        :param expected_codes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#expected_codes LoadBalancerMonitor#expected_codes}.
        :param follow_redirects: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#follow_redirects LoadBalancerMonitor#follow_redirects}.
        :param header: header block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#header LoadBalancerMonitor#header}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#id LoadBalancerMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interval: Defaults to ``60``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#interval LoadBalancerMonitor#interval}
        :param method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#method LoadBalancerMonitor#method}.
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#path LoadBalancerMonitor#path}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#port LoadBalancerMonitor#port}.
        :param probe_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#probe_zone LoadBalancerMonitor#probe_zone}.
        :param retries: Defaults to ``2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#retries LoadBalancerMonitor#retries}
        :param timeout: Defaults to ``5``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#timeout LoadBalancerMonitor#timeout}
        :param type: Defaults to ``http``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#type LoadBalancerMonitor#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b75f9f307aac8ba900193483d3a0ac09b91ca7087e3d1b1106211340baebc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LoadBalancerMonitorConfig(
            account_id=account_id,
            allow_insecure=allow_insecure,
            description=description,
            expected_body=expected_body,
            expected_codes=expected_codes,
            follow_redirects=follow_redirects,
            header=header,
            id=id,
            interval=interval,
            method=method,
            path=path,
            port=port,
            probe_zone=probe_zone,
            retries=retries,
            timeout=timeout,
            type=type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerMonitorHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28cd93805fb4a179f19c6150b821ac234e8288c45f24e4c3ad4cfcdc9ff54d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpectedBody")
    def reset_expected_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedBody", []))

    @jsii.member(jsii_name="resetExpectedCodes")
    def reset_expected_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedCodes", []))

    @jsii.member(jsii_name="resetFollowRedirects")
    def reset_follow_redirects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFollowRedirects", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProbeZone")
    def reset_probe_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProbeZone", []))

    @jsii.member(jsii_name="resetRetries")
    def reset_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetries", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> "LoadBalancerMonitorHeaderList":
        return typing.cast("LoadBalancerMonitorHeaderList", jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="modifiedOn")
    def modified_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedBodyInput")
    def expected_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expectedBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedCodesInput")
    def expected_codes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expectedCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="followRedirectsInput")
    def follow_redirects_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "followRedirectsInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerMonitorHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerMonitorHeader"]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="probeZoneInput")
    def probe_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "probeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="retriesInput")
    def retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retriesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6e0f6f90c973414c71a4be70826ff3be2afd02e2d706ddfde5219974debe39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6beddafc5ee834fed5fee1e25e9a4a9d931c17986bbdf8e09cb4a47d2bab30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad67f4db2792b65aee28d5c4acc9b15f253a40df0d460bab96af29d880c62fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="expectedBody")
    def expected_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expectedBody"))

    @expected_body.setter
    def expected_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e82a5ca69ee125134c82c09c27df91a16a8d9539fc6244a779a7bafb3c86eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedBody", value)

    @builtins.property
    @jsii.member(jsii_name="expectedCodes")
    def expected_codes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expectedCodes"))

    @expected_codes.setter
    def expected_codes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6e80a2c3d85077afc6d9c6fcd6d08d37322da75f3821e17a2c2587f1405513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedCodes", value)

    @builtins.property
    @jsii.member(jsii_name="followRedirects")
    def follow_redirects(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "followRedirects"))

    @follow_redirects.setter
    def follow_redirects(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974beeffe98b024405de715eb81b2365207e802c509d6a7a373319b3da7b69e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followRedirects", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3a22335bfa60202ca6ededdcc52f571efe8c2c1757fdda6c75f1cab3880d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce0b9714584d5625b6bfbb115e91ed4597cd3fd717f5bad6e01b9d75091c984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value)

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07fc0d913e0b0868490fe239848c1f5ef73f966d34c5f94ed21c42bc30c12391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e0a6e68bc6100a73fc1ac26b741062d94b5e197b3bab4d8f651a8ba2151bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408e841113b6b780bad647f0a987e98564961f8654dad23205e720dcab6cb935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="probeZone")
    def probe_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "probeZone"))

    @probe_zone.setter
    def probe_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134f739dd46249c968200e2fbe068dc780a284c1d65cf0eb1bd04d7bad1f3404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "probeZone", value)

    @builtins.property
    @jsii.member(jsii_name="retries")
    def retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retries"))

    @retries.setter
    def retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76a148923e383e054ee6b3c691d721d4f0ee30a6fd410c7dbc5db097dc75688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retries", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617129e10cbbd3a8e0c62fa43c985b6d91b488bc7966b20658d8ff4b9da2c88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86354f7c1825e807beb7861692e2a711dc515e0dfac48c82705651782ba1062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancerMonitor.LoadBalancerMonitorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "allow_insecure": "allowInsecure",
        "description": "description",
        "expected_body": "expectedBody",
        "expected_codes": "expectedCodes",
        "follow_redirects": "followRedirects",
        "header": "header",
        "id": "id",
        "interval": "interval",
        "method": "method",
        "path": "path",
        "port": "port",
        "probe_zone": "probeZone",
        "retries": "retries",
        "timeout": "timeout",
        "type": "type",
    },
)
class LoadBalancerMonitorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: typing.Optional[builtins.str] = None,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        expected_body: typing.Optional[builtins.str] = None,
        expected_codes: typing.Optional[builtins.str] = None,
        follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerMonitorHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        probe_zone: typing.Optional[builtins.str] = None,
        retries: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#account_id LoadBalancerMonitor#account_id}
        :param allow_insecure: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#allow_insecure LoadBalancerMonitor#allow_insecure}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#description LoadBalancerMonitor#description}.
        :param expected_body: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#expected_body LoadBalancerMonitor#expected_body}.
        :param expected_codes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#expected_codes LoadBalancerMonitor#expected_codes}.
        :param follow_redirects: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#follow_redirects LoadBalancerMonitor#follow_redirects}.
        :param header: header block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#header LoadBalancerMonitor#header}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#id LoadBalancerMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interval: Defaults to ``60``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#interval LoadBalancerMonitor#interval}
        :param method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#method LoadBalancerMonitor#method}.
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#path LoadBalancerMonitor#path}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#port LoadBalancerMonitor#port}.
        :param probe_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#probe_zone LoadBalancerMonitor#probe_zone}.
        :param retries: Defaults to ``2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#retries LoadBalancerMonitor#retries}
        :param timeout: Defaults to ``5``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#timeout LoadBalancerMonitor#timeout}
        :param type: Defaults to ``http``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#type LoadBalancerMonitor#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acdc2039e86d20dc5cbf863640102b49565274cdcd627502de3171e1ba5bc711)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expected_body", value=expected_body, expected_type=type_hints["expected_body"])
            check_type(argname="argument expected_codes", value=expected_codes, expected_type=type_hints["expected_codes"])
            check_type(argname="argument follow_redirects", value=follow_redirects, expected_type=type_hints["follow_redirects"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument probe_zone", value=probe_zone, expected_type=type_hints["probe_zone"])
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if description is not None:
            self._values["description"] = description
        if expected_body is not None:
            self._values["expected_body"] = expected_body
        if expected_codes is not None:
            self._values["expected_codes"] = expected_codes
        if follow_redirects is not None:
            self._values["follow_redirects"] = follow_redirects
        if header is not None:
            self._values["header"] = header
        if id is not None:
            self._values["id"] = id
        if interval is not None:
            self._values["interval"] = interval
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if probe_zone is not None:
            self._values["probe_zone"] = probe_zone
        if retries is not None:
            self._values["retries"] = retries
        if timeout is not None:
            self._values["timeout"] = timeout
        if type is not None:
            self._values["type"] = type

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
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#account_id LoadBalancerMonitor#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#allow_insecure LoadBalancerMonitor#allow_insecure}.'''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#description LoadBalancerMonitor#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_body(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#expected_body LoadBalancerMonitor#expected_body}.'''
        result = self._values.get("expected_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_codes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#expected_codes LoadBalancerMonitor#expected_codes}.'''
        result = self._values.get("expected_codes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def follow_redirects(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#follow_redirects LoadBalancerMonitor#follow_redirects}.'''
        result = self._values.get("follow_redirects")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerMonitorHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#header LoadBalancerMonitor#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerMonitorHeader"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#id LoadBalancerMonitor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Defaults to ``60``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#interval LoadBalancerMonitor#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#method LoadBalancerMonitor#method}.'''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#path LoadBalancerMonitor#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#port LoadBalancerMonitor#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def probe_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#probe_zone LoadBalancerMonitor#probe_zone}.'''
        result = self._values.get("probe_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''Defaults to ``2``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#retries LoadBalancerMonitor#retries}
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Defaults to ``5``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#timeout LoadBalancerMonitor#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Defaults to ``http``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#type LoadBalancerMonitor#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerMonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancerMonitor.LoadBalancerMonitorHeader",
    jsii_struct_bases=[],
    name_mapping={"header": "header", "values": "values"},
)
class LoadBalancerMonitorHeader:
    def __init__(
        self,
        *,
        header: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#header LoadBalancerMonitor#header}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#values LoadBalancerMonitor#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708b216b7682b8cf7105dbf0829da7c742aa01f0f7ced97bb078a39bdad0a704)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
            "values": values,
        }

    @builtins.property
    def header(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#header LoadBalancerMonitor#header}.'''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_monitor#values LoadBalancerMonitor#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerMonitorHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerMonitorHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerMonitor.LoadBalancerMonitorHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7e186183d658557e33112cef84f0fdb2376b1037ec1d3cb103360583061e834)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerMonitorHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c47967a578a9048c68a5963082e5472182a2bc0bd7e9d1a579fbce96c7b4ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerMonitorHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac735c3367207b8e5baab259bbbdf6616db536a196f301e81da2d1d2f11beb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31065ca2c9124622fe2d799182f859e2c5d7eecf23edc66cc44ea1fe61581586)
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
            type_hints = typing.get_type_hints(_typecheckingstub__328686d7f8483022c8c426faff07b83488a455df0dd48a9649f9b208fc030fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerMonitorHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerMonitorHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerMonitorHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f031ca5954dee030eb0ae46e612ab21a7b9760e29b0ffebdf78fe731ccca0b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerMonitorHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerMonitor.LoadBalancerMonitorHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9047ec2cfcc45b68b602ca9d70f375349aac56983d2d554806a4ef3f557bacab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885f10db46770d9e0b0e28930a0808fa47012d462c087920103e34dc28c65dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a6fb18fd79c80d6986d0251e513476663d9858fb09c108755048b845ea6ba3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerMonitorHeader, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerMonitorHeader, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerMonitorHeader, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d40d8f53bb68a132077509aa66f964dfb3d7ed4531abac45e8343d6a26a84ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LoadBalancerMonitor",
    "LoadBalancerMonitorConfig",
    "LoadBalancerMonitorHeader",
    "LoadBalancerMonitorHeaderList",
    "LoadBalancerMonitorHeaderOutputReference",
]

publication.publish()

def _typecheckingstub__02b75f9f307aac8ba900193483d3a0ac09b91ca7087e3d1b1106211340baebc3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: typing.Optional[builtins.str] = None,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    expected_body: typing.Optional[builtins.str] = None,
    expected_codes: typing.Optional[builtins.str] = None,
    follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerMonitorHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    probe_zone: typing.Optional[builtins.str] = None,
    retries: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b28cd93805fb4a179f19c6150b821ac234e8288c45f24e4c3ad4cfcdc9ff54d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerMonitorHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6e0f6f90c973414c71a4be70826ff3be2afd02e2d706ddfde5219974debe39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6beddafc5ee834fed5fee1e25e9a4a9d931c17986bbdf8e09cb4a47d2bab30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad67f4db2792b65aee28d5c4acc9b15f253a40df0d460bab96af29d880c62fea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e82a5ca69ee125134c82c09c27df91a16a8d9539fc6244a779a7bafb3c86eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6e80a2c3d85077afc6d9c6fcd6d08d37322da75f3821e17a2c2587f1405513(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974beeffe98b024405de715eb81b2365207e802c509d6a7a373319b3da7b69e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3a22335bfa60202ca6ededdcc52f571efe8c2c1757fdda6c75f1cab3880d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce0b9714584d5625b6bfbb115e91ed4597cd3fd717f5bad6e01b9d75091c984(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07fc0d913e0b0868490fe239848c1f5ef73f966d34c5f94ed21c42bc30c12391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e0a6e68bc6100a73fc1ac26b741062d94b5e197b3bab4d8f651a8ba2151bc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408e841113b6b780bad647f0a987e98564961f8654dad23205e720dcab6cb935(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134f739dd46249c968200e2fbe068dc780a284c1d65cf0eb1bd04d7bad1f3404(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76a148923e383e054ee6b3c691d721d4f0ee30a6fd410c7dbc5db097dc75688(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617129e10cbbd3a8e0c62fa43c985b6d91b488bc7966b20658d8ff4b9da2c88d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86354f7c1825e807beb7861692e2a711dc515e0dfac48c82705651782ba1062(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdc2039e86d20dc5cbf863640102b49565274cdcd627502de3171e1ba5bc711(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: typing.Optional[builtins.str] = None,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    expected_body: typing.Optional[builtins.str] = None,
    expected_codes: typing.Optional[builtins.str] = None,
    follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerMonitorHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    probe_zone: typing.Optional[builtins.str] = None,
    retries: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708b216b7682b8cf7105dbf0829da7c742aa01f0f7ced97bb078a39bdad0a704(
    *,
    header: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e186183d658557e33112cef84f0fdb2376b1037ec1d3cb103360583061e834(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c47967a578a9048c68a5963082e5472182a2bc0bd7e9d1a579fbce96c7b4ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac735c3367207b8e5baab259bbbdf6616db536a196f301e81da2d1d2f11beb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31065ca2c9124622fe2d799182f859e2c5d7eecf23edc66cc44ea1fe61581586(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328686d7f8483022c8c426faff07b83488a455df0dd48a9649f9b208fc030fe1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f031ca5954dee030eb0ae46e612ab21a7b9760e29b0ffebdf78fe731ccca0b00(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerMonitorHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9047ec2cfcc45b68b602ca9d70f375349aac56983d2d554806a4ef3f557bacab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885f10db46770d9e0b0e28930a0808fa47012d462c087920103e34dc28c65dc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6fb18fd79c80d6986d0251e513476663d9858fb09c108755048b845ea6ba3c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d40d8f53bb68a132077509aa66f964dfb3d7ed4531abac45e8343d6a26a84ee(
    value: typing.Optional[typing.Union[LoadBalancerMonitorHeader, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
