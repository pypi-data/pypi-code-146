'''
# `cloudflare_healthcheck`

Refer to the Terraform Registory for docs: [`cloudflare_healthcheck`](https://www.terraform.io/docs/providers/cloudflare/r/healthcheck).
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


class Healthcheck(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.healthcheck.Healthcheck",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck cloudflare_healthcheck}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        address: builtins.str,
        name: builtins.str,
        type: builtins.str,
        zone_id: builtins.str,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        consecutive_fails: typing.Optional[jsii.Number] = None,
        consecutive_successes: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        expected_body: typing.Optional[builtins.str] = None,
        expected_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcheckHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        retries: typing.Optional[jsii.Number] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["HealthcheckTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck cloudflare_healthcheck} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param address: The hostname or IP address of the origin server to run health checks on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#address Healthcheck#address}
        :param name: A short name to identify the health check. Only alphanumeric characters, hyphens, and underscores are allowed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#name Healthcheck#name}
        :param type: The protocol to use for the health check. Available values: ``TCP``, ``HTTP``, ``HTTPS``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#type Healthcheck#type}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#zone_id Healthcheck#zone_id}
        :param allow_insecure: Do not validate the certificate when the health check uses HTTPS. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#allow_insecure Healthcheck#allow_insecure}
        :param check_regions: A list of regions from which to run health checks. If not set, Cloudflare will pick a default region. Available values: ``WNAM``, ``ENAM``, ``WEU``, ``EEU``, ``NSAM``, ``SSAM``, ``OC``, ``ME``, ``NAF``, ``SAF``, ``IN``, ``SEAS``, ``NEAS``, ``ALL_REGIONS``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#check_regions Healthcheck#check_regions}
        :param consecutive_fails: The number of consecutive fails required from a health check before changing the health to unhealthy. Defaults to ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#consecutive_fails Healthcheck#consecutive_fails}
        :param consecutive_successes: The number of consecutive successes required from a health check before changing the health to healthy. Defaults to ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#consecutive_successes Healthcheck#consecutive_successes}
        :param description: A human-readable description of the health check. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#description Healthcheck#description}
        :param expected_body: A case-insensitive sub-string to look for in the response body. If this string is not found the origin will be marked as unhealthy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#expected_body Healthcheck#expected_body}
        :param expected_codes: The expected HTTP response codes (e.g. '200') or code ranges (e.g. '2xx' for all codes starting with 2) of the health check. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#expected_codes Healthcheck#expected_codes}
        :param follow_redirects: Follow redirects if the origin returns a 3xx status code. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#follow_redirects Healthcheck#follow_redirects}
        :param header: header block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#header Healthcheck#header}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#id Healthcheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interval: The interval between each health check. Shorter intervals may give quicker notifications if the origin status changes, but will increase the load on the origin as we check from multiple locations. Defaults to ``60``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#interval Healthcheck#interval}
        :param method: The HTTP method to use for the health check. Available values: ``connection_established``, ``GET``, ``HEAD``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#method Healthcheck#method}
        :param path: The endpoint path to health check against. Defaults to ``/``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#path Healthcheck#path}
        :param port: Port number to connect to for the health check. Defaults to ``80``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#port Healthcheck#port}
        :param retries: The number of retries to attempt in case of a timeout before marking the origin as unhealthy. Retries are attempted immediately. Defaults to ``2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#retries Healthcheck#retries}
        :param suspended: If suspended, no health checks are sent to the origin. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#suspended Healthcheck#suspended}
        :param timeout: The timeout (in seconds) before marking the health check as failed. Defaults to ``5``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#timeout Healthcheck#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#timeouts Healthcheck#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439c7a33345882300d035153d8c13854e1463bb3182c3f2489f3bc9a76b5a3aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HealthcheckConfig(
            address=address,
            name=name,
            type=type,
            zone_id=zone_id,
            allow_insecure=allow_insecure,
            check_regions=check_regions,
            consecutive_fails=consecutive_fails,
            consecutive_successes=consecutive_successes,
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
            retries=retries,
            suspended=suspended,
            timeout=timeout,
            timeouts=timeouts,
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcheckHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b3d7386cadd5a0458157127be6ee3b8beca185d350a72c9b417ad1399aa8b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#create Healthcheck#create}.
        '''
        value = HealthcheckTimeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetCheckRegions")
    def reset_check_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckRegions", []))

    @jsii.member(jsii_name="resetConsecutiveFails")
    def reset_consecutive_fails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsecutiveFails", []))

    @jsii.member(jsii_name="resetConsecutiveSuccesses")
    def reset_consecutive_successes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsecutiveSuccesses", []))

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

    @jsii.member(jsii_name="resetRetries")
    def reset_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetries", []))

    @jsii.member(jsii_name="resetSuspended")
    def reset_suspended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspended", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    def header(self) -> "HealthcheckHeaderList":
        return typing.cast("HealthcheckHeaderList", jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="modifiedOn")
    def modified_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HealthcheckTimeoutsOutputReference":
        return typing.cast("HealthcheckTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="checkRegionsInput")
    def check_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "checkRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="consecutiveFailsInput")
    def consecutive_fails_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "consecutiveFailsInput"))

    @builtins.property
    @jsii.member(jsii_name="consecutiveSuccessesInput")
    def consecutive_successes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "consecutiveSuccessesInput"))

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
    def expected_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "expectedCodesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcheckHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcheckHeader"]]], jsii.get(self, "headerInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="retriesInput")
    def retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retriesInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedInput")
    def suspended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suspendedInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["HealthcheckTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["HealthcheckTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a0145794d65eaf6483aabe9343f636aa1849456ef129f3741fc9fbe638484f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__1f7a076681675058ba3c77cbc35807b2316ed5d7479d2965a6466b9c62bbd3b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value)

    @builtins.property
    @jsii.member(jsii_name="checkRegions")
    def check_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "checkRegions"))

    @check_regions.setter
    def check_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7170e86651fbe5fe374bdb505422d79e10b707886e92a6dba98a246cac1801c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkRegions", value)

    @builtins.property
    @jsii.member(jsii_name="consecutiveFails")
    def consecutive_fails(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "consecutiveFails"))

    @consecutive_fails.setter
    def consecutive_fails(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b832331d709890a277852304cb7cabbc61131936ec2eb87cd28e73957b703a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveFails", value)

    @builtins.property
    @jsii.member(jsii_name="consecutiveSuccesses")
    def consecutive_successes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "consecutiveSuccesses"))

    @consecutive_successes.setter
    def consecutive_successes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1a1407b1ef1632cd65438995d00bf75c789f551ab1966e8f78fc2d4a33ea62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveSuccesses", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d59e1da0767586bfb78a9c7efda6ddd12035d1ccb791709e070d3863fe159b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="expectedBody")
    def expected_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expectedBody"))

    @expected_body.setter
    def expected_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb404a8dacd2b7b47f9080c8b121c2e850dcbe3b649a94183d088fc21fb7df69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedBody", value)

    @builtins.property
    @jsii.member(jsii_name="expectedCodes")
    def expected_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "expectedCodes"))

    @expected_codes.setter
    def expected_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1bbf27a94b11afc078b81ec01ce74a23918a165161d5b8b429f210b96f423f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__349b206707d510d79498931952c4555f6e3f86f223c68ab84428cb37341a424d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followRedirects", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0078fe9254a32a3880dec32589b80dec584592a449b17388dc0484e933fc4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355b7b2f13703688574c1c217437ec5ae64be8ad0a1495ecf6179c57190610f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value)

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289a517fd6c624468f133455b0fbe5010e8a5b7be0162bbf1d314ef5e58c14cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24568381d20f4b7643278e2871f5c9f2bbd732a265a36e789ef8ac5e559e2429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c03706f2cd1eb60111c061c0aa8066683ba2d14e19e3b7aae958e7e1ed68d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba4ea1800c089a6c1270fd91c11e0e86cb16a581fe1b0fb567cc465e4dcd476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="retries")
    def retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retries"))

    @retries.setter
    def retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119716033142fc1ad52f808a587b47dc240566d5f9cd6d8a1ab81c2fa19ab236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retries", value)

    @builtins.property
    @jsii.member(jsii_name="suspended")
    def suspended(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suspended"))

    @suspended.setter
    def suspended(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a19d1dba3106329c96b54e277fe06925f4b5c66e5faa8ee2a10c623a19dd12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cda692c7560946f77f666ab062d5a889bf96312fdcc691a767fa99499dd098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0e85db7756dd0fa7e242b5181178814ed7ee215bec091ae56044d0644f282f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fe6da7fdcdfa788113e368ede6e0b2f59218b5f1919029a2adaeae51c9475f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.healthcheck.HealthcheckConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "address": "address",
        "name": "name",
        "type": "type",
        "zone_id": "zoneId",
        "allow_insecure": "allowInsecure",
        "check_regions": "checkRegions",
        "consecutive_fails": "consecutiveFails",
        "consecutive_successes": "consecutiveSuccesses",
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
        "retries": "retries",
        "suspended": "suspended",
        "timeout": "timeout",
        "timeouts": "timeouts",
    },
)
class HealthcheckConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        address: builtins.str,
        name: builtins.str,
        type: builtins.str,
        zone_id: builtins.str,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        consecutive_fails: typing.Optional[jsii.Number] = None,
        consecutive_successes: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        expected_body: typing.Optional[builtins.str] = None,
        expected_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcheckHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        retries: typing.Optional[jsii.Number] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["HealthcheckTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param address: The hostname or IP address of the origin server to run health checks on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#address Healthcheck#address}
        :param name: A short name to identify the health check. Only alphanumeric characters, hyphens, and underscores are allowed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#name Healthcheck#name}
        :param type: The protocol to use for the health check. Available values: ``TCP``, ``HTTP``, ``HTTPS``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#type Healthcheck#type}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#zone_id Healthcheck#zone_id}
        :param allow_insecure: Do not validate the certificate when the health check uses HTTPS. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#allow_insecure Healthcheck#allow_insecure}
        :param check_regions: A list of regions from which to run health checks. If not set, Cloudflare will pick a default region. Available values: ``WNAM``, ``ENAM``, ``WEU``, ``EEU``, ``NSAM``, ``SSAM``, ``OC``, ``ME``, ``NAF``, ``SAF``, ``IN``, ``SEAS``, ``NEAS``, ``ALL_REGIONS``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#check_regions Healthcheck#check_regions}
        :param consecutive_fails: The number of consecutive fails required from a health check before changing the health to unhealthy. Defaults to ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#consecutive_fails Healthcheck#consecutive_fails}
        :param consecutive_successes: The number of consecutive successes required from a health check before changing the health to healthy. Defaults to ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#consecutive_successes Healthcheck#consecutive_successes}
        :param description: A human-readable description of the health check. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#description Healthcheck#description}
        :param expected_body: A case-insensitive sub-string to look for in the response body. If this string is not found the origin will be marked as unhealthy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#expected_body Healthcheck#expected_body}
        :param expected_codes: The expected HTTP response codes (e.g. '200') or code ranges (e.g. '2xx' for all codes starting with 2) of the health check. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#expected_codes Healthcheck#expected_codes}
        :param follow_redirects: Follow redirects if the origin returns a 3xx status code. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#follow_redirects Healthcheck#follow_redirects}
        :param header: header block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#header Healthcheck#header}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#id Healthcheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interval: The interval between each health check. Shorter intervals may give quicker notifications if the origin status changes, but will increase the load on the origin as we check from multiple locations. Defaults to ``60``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#interval Healthcheck#interval}
        :param method: The HTTP method to use for the health check. Available values: ``connection_established``, ``GET``, ``HEAD``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#method Healthcheck#method}
        :param path: The endpoint path to health check against. Defaults to ``/``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#path Healthcheck#path}
        :param port: Port number to connect to for the health check. Defaults to ``80``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#port Healthcheck#port}
        :param retries: The number of retries to attempt in case of a timeout before marking the origin as unhealthy. Retries are attempted immediately. Defaults to ``2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#retries Healthcheck#retries}
        :param suspended: If suspended, no health checks are sent to the origin. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#suspended Healthcheck#suspended}
        :param timeout: The timeout (in seconds) before marking the health check as failed. Defaults to ``5``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#timeout Healthcheck#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#timeouts Healthcheck#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = HealthcheckTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0424666b11c4e7ec247698af28f912f8e859d7841cf6349e831e754e943b3d3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument check_regions", value=check_regions, expected_type=type_hints["check_regions"])
            check_type(argname="argument consecutive_fails", value=consecutive_fails, expected_type=type_hints["consecutive_fails"])
            check_type(argname="argument consecutive_successes", value=consecutive_successes, expected_type=type_hints["consecutive_successes"])
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
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "name": name,
            "type": type,
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
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if check_regions is not None:
            self._values["check_regions"] = check_regions
        if consecutive_fails is not None:
            self._values["consecutive_fails"] = consecutive_fails
        if consecutive_successes is not None:
            self._values["consecutive_successes"] = consecutive_successes
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
        if retries is not None:
            self._values["retries"] = retries
        if suspended is not None:
            self._values["suspended"] = suspended
        if timeout is not None:
            self._values["timeout"] = timeout
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def address(self) -> builtins.str:
        '''The hostname or IP address of the origin server to run health checks on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#address Healthcheck#address}
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A short name to identify the health check. Only alphanumeric characters, hyphens, and underscores are allowed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#name Healthcheck#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The protocol to use for the health check. Available values: ``TCP``, ``HTTP``, ``HTTPS``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#type Healthcheck#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#zone_id Healthcheck#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not validate the certificate when the health check uses HTTPS. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#allow_insecure Healthcheck#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def check_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of regions from which to run health checks.

        If not set, Cloudflare will pick a default region. Available values: ``WNAM``, ``ENAM``, ``WEU``, ``EEU``, ``NSAM``, ``SSAM``, ``OC``, ``ME``, ``NAF``, ``SAF``, ``IN``, ``SEAS``, ``NEAS``, ``ALL_REGIONS``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#check_regions Healthcheck#check_regions}
        '''
        result = self._values.get("check_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def consecutive_fails(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive fails required from a health check before changing the health to unhealthy. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#consecutive_fails Healthcheck#consecutive_fails}
        '''
        result = self._values.get("consecutive_fails")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consecutive_successes(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive successes required from a health check before changing the health to healthy. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#consecutive_successes Healthcheck#consecutive_successes}
        '''
        result = self._values.get("consecutive_successes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the health check.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#description Healthcheck#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_body(self) -> typing.Optional[builtins.str]:
        '''A case-insensitive sub-string to look for in the response body.

        If this string is not found the origin will be marked as unhealthy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#expected_body Healthcheck#expected_body}
        '''
        result = self._values.get("expected_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The expected HTTP response codes (e.g. '200') or code ranges (e.g. '2xx' for all codes starting with 2) of the health check.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#expected_codes Healthcheck#expected_codes}
        '''
        result = self._values.get("expected_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow_redirects(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Follow redirects if the origin returns a 3xx status code. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#follow_redirects Healthcheck#follow_redirects}
        '''
        result = self._values.get("follow_redirects")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcheckHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#header Healthcheck#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcheckHeader"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#id Healthcheck#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''The interval between each health check.

        Shorter intervals may give quicker notifications if the origin status changes, but will increase the load on the origin as we check from multiple locations. Defaults to ``60``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#interval Healthcheck#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''The HTTP method to use for the health check. Available values: ``connection_established``, ``GET``, ``HEAD``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#method Healthcheck#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The endpoint path to health check against. Defaults to ``/``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#path Healthcheck#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to connect to for the health check. Defaults to ``80``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#port Healthcheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''The number of retries to attempt in case of a timeout before marking the origin as unhealthy.

        Retries are attempted immediately. Defaults to ``2``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#retries Healthcheck#retries}
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If suspended, no health checks are sent to the origin. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#suspended Healthcheck#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout (in seconds) before marking the health check as failed. Defaults to ``5``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#timeout Healthcheck#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HealthcheckTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#timeouts Healthcheck#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HealthcheckTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcheckConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.healthcheck.HealthcheckHeader",
    jsii_struct_bases=[],
    name_mapping={"header": "header", "values": "values"},
)
class HealthcheckHeader:
    def __init__(
        self,
        *,
        header: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param header: The header name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#header Healthcheck#header}
        :param values: A list of string values for the header. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#values Healthcheck#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6116e2515ac2f35dbe2afb8199a42c18280c91746038586d61ebcba505ca03)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
            "values": values,
        }

    @builtins.property
    def header(self) -> builtins.str:
        '''The header name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#header Healthcheck#header}
        '''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''A list of string values for the header.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#values Healthcheck#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcheckHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcheckHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.healthcheck.HealthcheckHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c2e48d8fef51fe28c4f20c73933901b0e947abe41cde6a269c877799ee6e16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "HealthcheckHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fa7e647f2f33ada5ea7e966c33a41cff957c94fd0cf1047179ffc2e45b9df5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HealthcheckHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6612bd2e518bf48a20083b7fe32c82694690468c241525a49dd51bcd8d7cb101)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14c926645efb19c05ce6e37e4c04ca6e2aa2d4a5882c37e38875b7528c5a67e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9344a80614d7c64b94048528d675a7530a79524af726542b2f78b3ad8ec4663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcheckHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcheckHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcheckHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4bd416d8a18f8704ecb6ca264aeff6502dbe328b8e5de3e8a5d3a4ca2f5737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class HealthcheckHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.healthcheck.HealthcheckHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc235063efe292ec1e48e4ed5a97d4ee61164c2fa737c3eb1b59b9fb0c4a355e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bed8a62c8bba90119fa013f56ee2e244f830c9f4fcabd30ecdea7d002955f8ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e15318b4f547cb22260a64419a9fe93641b3c7bd086708c3bae73560ad5b4c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[HealthcheckHeader, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[HealthcheckHeader, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[HealthcheckHeader, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da68ccfeb05e50b27cc074f9a7bb2e4e5fbc1bbfb95b28b0d374cf774150971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.healthcheck.HealthcheckTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class HealthcheckTimeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#create Healthcheck#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3931e781cdec3a3e026a4f0d23c739d97daa5aecfa6c0f809299ccfe5f8ea10f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/healthcheck#create Healthcheck#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcheckTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcheckTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.healthcheck.HealthcheckTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5704339b890207bbcb3766d9f5a10325397581313c7907433448891fb936396a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3ccbde57fec7a4e9e0115fdf4490b11201c4bcab9b6d290a2c8886f01eeb63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[HealthcheckTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[HealthcheckTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[HealthcheckTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb56e8337b48de362c7f241a04175d2fa74707bf92a60b71f841c4d2a6b32b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Healthcheck",
    "HealthcheckConfig",
    "HealthcheckHeader",
    "HealthcheckHeaderList",
    "HealthcheckHeaderOutputReference",
    "HealthcheckTimeouts",
    "HealthcheckTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__439c7a33345882300d035153d8c13854e1463bb3182c3f2489f3bc9a76b5a3aa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    address: builtins.str,
    name: builtins.str,
    type: builtins.str,
    zone_id: builtins.str,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    consecutive_fails: typing.Optional[jsii.Number] = None,
    consecutive_successes: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    expected_body: typing.Optional[builtins.str] = None,
    expected_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcheckHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    retries: typing.Optional[jsii.Number] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[HealthcheckTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b4b3d7386cadd5a0458157127be6ee3b8beca185d350a72c9b417ad1399aa8b0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcheckHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a0145794d65eaf6483aabe9343f636aa1849456ef129f3741fc9fbe638484f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7a076681675058ba3c77cbc35807b2316ed5d7479d2965a6466b9c62bbd3b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7170e86651fbe5fe374bdb505422d79e10b707886e92a6dba98a246cac1801c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b832331d709890a277852304cb7cabbc61131936ec2eb87cd28e73957b703a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1a1407b1ef1632cd65438995d00bf75c789f551ab1966e8f78fc2d4a33ea62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d59e1da0767586bfb78a9c7efda6ddd12035d1ccb791709e070d3863fe159b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb404a8dacd2b7b47f9080c8b121c2e850dcbe3b649a94183d088fc21fb7df69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1bbf27a94b11afc078b81ec01ce74a23918a165161d5b8b429f210b96f423f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349b206707d510d79498931952c4555f6e3f86f223c68ab84428cb37341a424d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0078fe9254a32a3880dec32589b80dec584592a449b17388dc0484e933fc4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355b7b2f13703688574c1c217437ec5ae64be8ad0a1495ecf6179c57190610f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289a517fd6c624468f133455b0fbe5010e8a5b7be0162bbf1d314ef5e58c14cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24568381d20f4b7643278e2871f5c9f2bbd732a265a36e789ef8ac5e559e2429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c03706f2cd1eb60111c061c0aa8066683ba2d14e19e3b7aae958e7e1ed68d39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba4ea1800c089a6c1270fd91c11e0e86cb16a581fe1b0fb567cc465e4dcd476(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119716033142fc1ad52f808a587b47dc240566d5f9cd6d8a1ab81c2fa19ab236(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a19d1dba3106329c96b54e277fe06925f4b5c66e5faa8ee2a10c623a19dd12(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cda692c7560946f77f666ab062d5a889bf96312fdcc691a767fa99499dd098(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0e85db7756dd0fa7e242b5181178814ed7ee215bec091ae56044d0644f282f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fe6da7fdcdfa788113e368ede6e0b2f59218b5f1919029a2adaeae51c9475f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0424666b11c4e7ec247698af28f912f8e859d7841cf6349e831e754e943b3d3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    address: builtins.str,
    name: builtins.str,
    type: builtins.str,
    zone_id: builtins.str,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    consecutive_fails: typing.Optional[jsii.Number] = None,
    consecutive_successes: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    expected_body: typing.Optional[builtins.str] = None,
    expected_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_redirects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcheckHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    retries: typing.Optional[jsii.Number] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[HealthcheckTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6116e2515ac2f35dbe2afb8199a42c18280c91746038586d61ebcba505ca03(
    *,
    header: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c2e48d8fef51fe28c4f20c73933901b0e947abe41cde6a269c877799ee6e16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fa7e647f2f33ada5ea7e966c33a41cff957c94fd0cf1047179ffc2e45b9df5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6612bd2e518bf48a20083b7fe32c82694690468c241525a49dd51bcd8d7cb101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c926645efb19c05ce6e37e4c04ca6e2aa2d4a5882c37e38875b7528c5a67e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9344a80614d7c64b94048528d675a7530a79524af726542b2f78b3ad8ec4663(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4bd416d8a18f8704ecb6ca264aeff6502dbe328b8e5de3e8a5d3a4ca2f5737(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcheckHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc235063efe292ec1e48e4ed5a97d4ee61164c2fa737c3eb1b59b9fb0c4a355e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed8a62c8bba90119fa013f56ee2e244f830c9f4fcabd30ecdea7d002955f8ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e15318b4f547cb22260a64419a9fe93641b3c7bd086708c3bae73560ad5b4c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da68ccfeb05e50b27cc074f9a7bb2e4e5fbc1bbfb95b28b0d374cf774150971(
    value: typing.Optional[typing.Union[HealthcheckHeader, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3931e781cdec3a3e026a4f0d23c739d97daa5aecfa6c0f809299ccfe5f8ea10f(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5704339b890207bbcb3766d9f5a10325397581313c7907433448891fb936396a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3ccbde57fec7a4e9e0115fdf4490b11201c4bcab9b6d290a2c8886f01eeb63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb56e8337b48de362c7f241a04175d2fa74707bf92a60b71f841c4d2a6b32b1(
    value: typing.Optional[typing.Union[HealthcheckTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
