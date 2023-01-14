'''
# `aws_route53_record`

Refer to the Terraform Registory for docs: [`aws_route53_record`](https://www.terraform.io/docs/providers/aws/r/route53_record).
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


class Route53Record(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53Record",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/route53_record aws_route53_record}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        zone_id: builtins.str,
        alias: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordAlias", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allow_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordFailoverRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        geolocation_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordGeolocationRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_check_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        latency_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordLatencyRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        multivalue_answer_routing_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        records: typing.Optional[typing.Sequence[builtins.str]] = None,
        set_identifier: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
        weighted_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordWeightedRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/route53_record aws_route53_record} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#name Route53Record#name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#type Route53Record#type}.
        :param zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#zone_id Route53Record#zone_id}.
        :param alias: alias block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#alias Route53Record#alias}
        :param allow_overwrite: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#allow_overwrite Route53Record#allow_overwrite}.
        :param failover_routing_policy: failover_routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#failover_routing_policy Route53Record#failover_routing_policy}
        :param geolocation_routing_policy: geolocation_routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#geolocation_routing_policy Route53Record#geolocation_routing_policy}
        :param health_check_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#health_check_id Route53Record#health_check_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#id Route53Record#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param latency_routing_policy: latency_routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#latency_routing_policy Route53Record#latency_routing_policy}
        :param multivalue_answer_routing_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#multivalue_answer_routing_policy Route53Record#multivalue_answer_routing_policy}.
        :param records: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#records Route53Record#records}.
        :param set_identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#set_identifier Route53Record#set_identifier}.
        :param ttl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#ttl Route53Record#ttl}.
        :param weighted_routing_policy: weighted_routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#weighted_routing_policy Route53Record#weighted_routing_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f5b59686cb8993858d6d7b9d56fb53382192067cad2c01362d14ebaaaec159)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Route53RecordConfig(
            name=name,
            type=type,
            zone_id=zone_id,
            alias=alias,
            allow_overwrite=allow_overwrite,
            failover_routing_policy=failover_routing_policy,
            geolocation_routing_policy=geolocation_routing_policy,
            health_check_id=health_check_id,
            id=id,
            latency_routing_policy=latency_routing_policy,
            multivalue_answer_routing_policy=multivalue_answer_routing_policy,
            records=records,
            set_identifier=set_identifier,
            ttl=ttl,
            weighted_routing_policy=weighted_routing_policy,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAlias")
    def put_alias(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordAlias", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2739e121e7c9f7d2b606d3e41d5c6bb67761d240bcd585c19f559c6e7b89178d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAlias", [value]))

    @jsii.member(jsii_name="putFailoverRoutingPolicy")
    def put_failover_routing_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordFailoverRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a7e6d94ecc1e0e93cb4ab10dde2a0536ab7d8a6a8274dfb5a2cce4702e9196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFailoverRoutingPolicy", [value]))

    @jsii.member(jsii_name="putGeolocationRoutingPolicy")
    def put_geolocation_routing_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordGeolocationRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8410655fccd5114e61473d2de25656c368919e9ba62bf876bfa558659ea1018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGeolocationRoutingPolicy", [value]))

    @jsii.member(jsii_name="putLatencyRoutingPolicy")
    def put_latency_routing_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordLatencyRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ecb8be5f80e5732495d4ccc8f0a60874d3a9ead0f8e1f79e6a60682890aaf99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLatencyRoutingPolicy", [value]))

    @jsii.member(jsii_name="putWeightedRoutingPolicy")
    def put_weighted_routing_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordWeightedRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de79ba6bae13ff08c95efdc70144fafeaf57314e9e456db382e400597a7fd849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeightedRoutingPolicy", [value]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAllowOverwrite")
    def reset_allow_overwrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowOverwrite", []))

    @jsii.member(jsii_name="resetFailoverRoutingPolicy")
    def reset_failover_routing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverRoutingPolicy", []))

    @jsii.member(jsii_name="resetGeolocationRoutingPolicy")
    def reset_geolocation_routing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeolocationRoutingPolicy", []))

    @jsii.member(jsii_name="resetHealthCheckId")
    def reset_health_check_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLatencyRoutingPolicy")
    def reset_latency_routing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatencyRoutingPolicy", []))

    @jsii.member(jsii_name="resetMultivalueAnswerRoutingPolicy")
    def reset_multivalue_answer_routing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultivalueAnswerRoutingPolicy", []))

    @jsii.member(jsii_name="resetRecords")
    def reset_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecords", []))

    @jsii.member(jsii_name="resetSetIdentifier")
    def reset_set_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetIdentifier", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @jsii.member(jsii_name="resetWeightedRoutingPolicy")
    def reset_weighted_routing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeightedRoutingPolicy", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> "Route53RecordAliasList":
        return typing.cast("Route53RecordAliasList", jsii.get(self, "alias"))

    @builtins.property
    @jsii.member(jsii_name="failoverRoutingPolicy")
    def failover_routing_policy(self) -> "Route53RecordFailoverRoutingPolicyList":
        return typing.cast("Route53RecordFailoverRoutingPolicyList", jsii.get(self, "failoverRoutingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="geolocationRoutingPolicy")
    def geolocation_routing_policy(self) -> "Route53RecordGeolocationRoutingPolicyList":
        return typing.cast("Route53RecordGeolocationRoutingPolicyList", jsii.get(self, "geolocationRoutingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="latencyRoutingPolicy")
    def latency_routing_policy(self) -> "Route53RecordLatencyRoutingPolicyList":
        return typing.cast("Route53RecordLatencyRoutingPolicyList", jsii.get(self, "latencyRoutingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="weightedRoutingPolicy")
    def weighted_routing_policy(self) -> "Route53RecordWeightedRoutingPolicyList":
        return typing.cast("Route53RecordWeightedRoutingPolicyList", jsii.get(self, "weightedRoutingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordAlias"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordAlias"]]], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOverwriteInput")
    def allow_overwrite_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowOverwriteInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverRoutingPolicyInput")
    def failover_routing_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordFailoverRoutingPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordFailoverRoutingPolicy"]]], jsii.get(self, "failoverRoutingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="geolocationRoutingPolicyInput")
    def geolocation_routing_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordGeolocationRoutingPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordGeolocationRoutingPolicy"]]], jsii.get(self, "geolocationRoutingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckIdInput")
    def health_check_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="latencyRoutingPolicyInput")
    def latency_routing_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordLatencyRoutingPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordLatencyRoutingPolicy"]]], jsii.get(self, "latencyRoutingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="multivalueAnswerRoutingPolicyInput")
    def multivalue_answer_routing_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multivalueAnswerRoutingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="recordsInput")
    def records_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "recordsInput"))

    @builtins.property
    @jsii.member(jsii_name="setIdentifierInput")
    def set_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "setIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="weightedRoutingPolicyInput")
    def weighted_routing_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordWeightedRoutingPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordWeightedRoutingPolicy"]]], jsii.get(self, "weightedRoutingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOverwrite")
    def allow_overwrite(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowOverwrite"))

    @allow_overwrite.setter
    def allow_overwrite(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e822ce13c0c1f2e6ef47533cdceac5bfebf68ff7a84983a23ce3142acff7692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOverwrite", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckId"))

    @health_check_id.setter
    def health_check_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5153b07b556a8e4336b215a9ba774b26a360439749b4337716c51c08dcde9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c46a03e80f09759a3049111f9214bf31cf381fed6e82f241daa93db2a96dbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="multivalueAnswerRoutingPolicy")
    def multivalue_answer_routing_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multivalueAnswerRoutingPolicy"))

    @multivalue_answer_routing_policy.setter
    def multivalue_answer_routing_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ecdf8a17309c19c46d4597e276e1a5d83bce2ffaea7ddf4ebaa98f4cdd933a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multivalueAnswerRoutingPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f69796a27e7ae2954e5965d462a7b6f58c32b03353caa20e077c603d983ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="records")
    def records(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "records"))

    @records.setter
    def records(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cfb6d133f3c765dbb87b21ce121c5a32f64e35564ad68c03fd612cb816a0bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "records", value)

    @builtins.property
    @jsii.member(jsii_name="setIdentifier")
    def set_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "setIdentifier"))

    @set_identifier.setter
    def set_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e4edbcc53ac0eb95a961a293ef2f1f3a7dcecdb147f1cd8c602851748d78a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4774f1276093a280f9a33c1b88caadae84b4cf48d49f52399845c07a58a711c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b5957ba08d59ec45d652bff2891ef182ee4567633239591697615016fb2af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6efc358fb10951b3d3f705725c430cf900d1c59597b44f689f99ccbd2e6df63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordAlias",
    jsii_struct_bases=[],
    name_mapping={
        "evaluate_target_health": "evaluateTargetHealth",
        "name": "name",
        "zone_id": "zoneId",
    },
)
class Route53RecordAlias:
    def __init__(
        self,
        *,
        evaluate_target_health: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        zone_id: builtins.str,
    ) -> None:
        '''
        :param evaluate_target_health: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#evaluate_target_health Route53Record#evaluate_target_health}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#name Route53Record#name}.
        :param zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#zone_id Route53Record#zone_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ad3458a72faf84e447106807b17f77177e205dcbf6498b3b7d74ee4c28b6d6)
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "evaluate_target_health": evaluate_target_health,
            "name": name,
            "zone_id": zone_id,
        }

    @builtins.property
    def evaluate_target_health(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#evaluate_target_health Route53Record#evaluate_target_health}.'''
        result = self._values.get("evaluate_target_health")
        assert result is not None, "Required property 'evaluate_target_health' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#name Route53Record#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#zone_id Route53Record#zone_id}.'''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53RecordAlias(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53RecordAliasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordAliasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c330e65508bfb3fe36ea6c3b9eace58ad220a72a5f5617001100a95512ced9a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "Route53RecordAliasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8efd785bb1e39ee786671457bcccfc24b92fdcacff0366a4222779161519c6a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Route53RecordAliasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1abc1fb8420e3f04f233070f9486efee72dad232a0839ff3d714be480cb97a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbba7b694900fbb5a30db495a965d776387fa8d3810c3e2582c4d7d7b6841f3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11c448a1ea8bdb4bcec68dccffd450cbb3e64d16e0012bca0d32448cbfda55ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordAlias]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordAlias]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordAlias]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d6a6c861af2a6998f957034aa71f9dd2eb0b4b3f070e5784e10ca7276468af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class Route53RecordAliasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordAliasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2362a0284f0d13d848404a01d5524e028c28a3fb4c1dfed5ccb7e4ab40dd8511)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="evaluateTargetHealthInput")
    def evaluate_target_health_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "evaluateTargetHealthInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluateTargetHealth")
    def evaluate_target_health(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "evaluateTargetHealth"))

    @evaluate_target_health.setter
    def evaluate_target_health(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9828de0792ad65f7b056035a7f17abd8dbfed011972bb68f39c73d282dc335f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluateTargetHealth", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3069dca3a23be24e3e1ad2455a847bcf6a73229a610344df23a45cc98d4e665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2f575aac87161cfd818203c422e61dd24c064cea63eafc1e9c884327b2996c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[Route53RecordAlias, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[Route53RecordAlias, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[Route53RecordAlias, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042c8287bf7bc43b15d5320b876fa8bfa486458002db5dc11567d82fe956f751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordConfig",
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
        "type": "type",
        "zone_id": "zoneId",
        "alias": "alias",
        "allow_overwrite": "allowOverwrite",
        "failover_routing_policy": "failoverRoutingPolicy",
        "geolocation_routing_policy": "geolocationRoutingPolicy",
        "health_check_id": "healthCheckId",
        "id": "id",
        "latency_routing_policy": "latencyRoutingPolicy",
        "multivalue_answer_routing_policy": "multivalueAnswerRoutingPolicy",
        "records": "records",
        "set_identifier": "setIdentifier",
        "ttl": "ttl",
        "weighted_routing_policy": "weightedRoutingPolicy",
    },
)
class Route53RecordConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        zone_id: builtins.str,
        alias: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordAlias, typing.Dict[builtins.str, typing.Any]]]]] = None,
        allow_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordFailoverRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        geolocation_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordGeolocationRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_check_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        latency_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordLatencyRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        multivalue_answer_routing_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        records: typing.Optional[typing.Sequence[builtins.str]] = None,
        set_identifier: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
        weighted_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53RecordWeightedRoutingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#name Route53Record#name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#type Route53Record#type}.
        :param zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#zone_id Route53Record#zone_id}.
        :param alias: alias block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#alias Route53Record#alias}
        :param allow_overwrite: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#allow_overwrite Route53Record#allow_overwrite}.
        :param failover_routing_policy: failover_routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#failover_routing_policy Route53Record#failover_routing_policy}
        :param geolocation_routing_policy: geolocation_routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#geolocation_routing_policy Route53Record#geolocation_routing_policy}
        :param health_check_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#health_check_id Route53Record#health_check_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#id Route53Record#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param latency_routing_policy: latency_routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#latency_routing_policy Route53Record#latency_routing_policy}
        :param multivalue_answer_routing_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#multivalue_answer_routing_policy Route53Record#multivalue_answer_routing_policy}.
        :param records: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#records Route53Record#records}.
        :param set_identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#set_identifier Route53Record#set_identifier}.
        :param ttl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#ttl Route53Record#ttl}.
        :param weighted_routing_policy: weighted_routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#weighted_routing_policy Route53Record#weighted_routing_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1842bebe04831c413fc865c1760274061405c09f54bcf3093b64252b4cd4baad)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allow_overwrite", value=allow_overwrite, expected_type=type_hints["allow_overwrite"])
            check_type(argname="argument failover_routing_policy", value=failover_routing_policy, expected_type=type_hints["failover_routing_policy"])
            check_type(argname="argument geolocation_routing_policy", value=geolocation_routing_policy, expected_type=type_hints["geolocation_routing_policy"])
            check_type(argname="argument health_check_id", value=health_check_id, expected_type=type_hints["health_check_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument latency_routing_policy", value=latency_routing_policy, expected_type=type_hints["latency_routing_policy"])
            check_type(argname="argument multivalue_answer_routing_policy", value=multivalue_answer_routing_policy, expected_type=type_hints["multivalue_answer_routing_policy"])
            check_type(argname="argument records", value=records, expected_type=type_hints["records"])
            check_type(argname="argument set_identifier", value=set_identifier, expected_type=type_hints["set_identifier"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument weighted_routing_policy", value=weighted_routing_policy, expected_type=type_hints["weighted_routing_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if alias is not None:
            self._values["alias"] = alias
        if allow_overwrite is not None:
            self._values["allow_overwrite"] = allow_overwrite
        if failover_routing_policy is not None:
            self._values["failover_routing_policy"] = failover_routing_policy
        if geolocation_routing_policy is not None:
            self._values["geolocation_routing_policy"] = geolocation_routing_policy
        if health_check_id is not None:
            self._values["health_check_id"] = health_check_id
        if id is not None:
            self._values["id"] = id
        if latency_routing_policy is not None:
            self._values["latency_routing_policy"] = latency_routing_policy
        if multivalue_answer_routing_policy is not None:
            self._values["multivalue_answer_routing_policy"] = multivalue_answer_routing_policy
        if records is not None:
            self._values["records"] = records
        if set_identifier is not None:
            self._values["set_identifier"] = set_identifier
        if ttl is not None:
            self._values["ttl"] = ttl
        if weighted_routing_policy is not None:
            self._values["weighted_routing_policy"] = weighted_routing_policy

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#name Route53Record#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#type Route53Record#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#zone_id Route53Record#zone_id}.'''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordAlias]]]:
        '''alias block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#alias Route53Record#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordAlias]]], result)

    @builtins.property
    def allow_overwrite(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#allow_overwrite Route53Record#allow_overwrite}.'''
        result = self._values.get("allow_overwrite")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def failover_routing_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordFailoverRoutingPolicy"]]]:
        '''failover_routing_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#failover_routing_policy Route53Record#failover_routing_policy}
        '''
        result = self._values.get("failover_routing_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordFailoverRoutingPolicy"]]], result)

    @builtins.property
    def geolocation_routing_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordGeolocationRoutingPolicy"]]]:
        '''geolocation_routing_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#geolocation_routing_policy Route53Record#geolocation_routing_policy}
        '''
        result = self._values.get("geolocation_routing_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordGeolocationRoutingPolicy"]]], result)

    @builtins.property
    def health_check_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#health_check_id Route53Record#health_check_id}.'''
        result = self._values.get("health_check_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#id Route53Record#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def latency_routing_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordLatencyRoutingPolicy"]]]:
        '''latency_routing_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#latency_routing_policy Route53Record#latency_routing_policy}
        '''
        result = self._values.get("latency_routing_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordLatencyRoutingPolicy"]]], result)

    @builtins.property
    def multivalue_answer_routing_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#multivalue_answer_routing_policy Route53Record#multivalue_answer_routing_policy}.'''
        result = self._values.get("multivalue_answer_routing_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def records(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#records Route53Record#records}.'''
        result = self._values.get("records")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def set_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#set_identifier Route53Record#set_identifier}.'''
        result = self._values.get("set_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#ttl Route53Record#ttl}.'''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weighted_routing_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordWeightedRoutingPolicy"]]]:
        '''weighted_routing_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#weighted_routing_policy Route53Record#weighted_routing_policy}
        '''
        result = self._values.get("weighted_routing_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53RecordWeightedRoutingPolicy"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53RecordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordFailoverRoutingPolicy",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class Route53RecordFailoverRoutingPolicy:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#type Route53Record#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce0183eff110b972fee5a66acf0258247d1029d0f2a719bf041bb22d7f900bc)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#type Route53Record#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53RecordFailoverRoutingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53RecordFailoverRoutingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordFailoverRoutingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd4b68ebd030e48b5e9b5d807510f980514f53fa06d7f21c0d10a1bde7b9b92f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Route53RecordFailoverRoutingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b3c0769945812f977d9c97959df7d4a24339e96bf5e3b4b0c56fe3d13add99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Route53RecordFailoverRoutingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f70c1dc3989de544c993b5661f04b07e92119a3445a366629390ba40ecf2b7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e03fd3f47102053e9f49cab8e674d38503c7b35e1c4d3fbbff3279080be0fedc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5cd63b34d64e272ea5e8b1cdeaf0e8217600e35e37256c71f50c38e188adced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordFailoverRoutingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordFailoverRoutingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordFailoverRoutingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9310c7823a8b1c6f3b93d7d460a454443103d038e675be8d5f0733e943cac051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class Route53RecordFailoverRoutingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordFailoverRoutingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cc079ac9358a23334e259a945ac81122d8583217d2dc10a8a73f8e3a0dbc097)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894be4fefe07e574ad08fcff21f9996be1b2319991c5c03cfe4cba33e64c6926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[Route53RecordFailoverRoutingPolicy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[Route53RecordFailoverRoutingPolicy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[Route53RecordFailoverRoutingPolicy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324ce71ecd0de1538bf9491d47f3ae9bfe952378173963353ee0ad633066898e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordGeolocationRoutingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "continent": "continent",
        "country": "country",
        "subdivision": "subdivision",
    },
)
class Route53RecordGeolocationRoutingPolicy:
    def __init__(
        self,
        *,
        continent: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        subdivision: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param continent: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#continent Route53Record#continent}.
        :param country: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#country Route53Record#country}.
        :param subdivision: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#subdivision Route53Record#subdivision}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6b879ebb9bb510894d0f3fd3daa9a59d5c73af6a5a1e92636c597f68c25981)
            check_type(argname="argument continent", value=continent, expected_type=type_hints["continent"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument subdivision", value=subdivision, expected_type=type_hints["subdivision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continent is not None:
            self._values["continent"] = continent
        if country is not None:
            self._values["country"] = country
        if subdivision is not None:
            self._values["subdivision"] = subdivision

    @builtins.property
    def continent(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#continent Route53Record#continent}.'''
        result = self._values.get("continent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#country Route53Record#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdivision(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#subdivision Route53Record#subdivision}.'''
        result = self._values.get("subdivision")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53RecordGeolocationRoutingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53RecordGeolocationRoutingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordGeolocationRoutingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4b63c1516a16b05a941000bb1485db715638a3ce1996ccb96ce1ce9bde79159)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Route53RecordGeolocationRoutingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27fb9a80d129007b7e99fa6c4eef4b9948ddc479d698f2668029a18433733621)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Route53RecordGeolocationRoutingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72a8e493d5cbb9966f28295e5a155e14ac1158b55aa67f83a463dab23093011)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e3882a4abb54c93685ebf22c0cf5e3234dbbc6d43543d3a865e2436f3605ac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ad1a6eea3062048d0cd2133d2a6cf16c810c0d9ab27633b1ba290d0e15e9bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordGeolocationRoutingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordGeolocationRoutingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordGeolocationRoutingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d42a4169deb5ff0f78c6f6f08dcb61354da572c3a8b2adab77a9dcf451164c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class Route53RecordGeolocationRoutingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordGeolocationRoutingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88a7d46d635871cb83cb285ca11cc163e9070c04923b7313127c60b086f8bf0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContinent")
    def reset_continent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinent", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetSubdivision")
    def reset_subdivision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubdivision", []))

    @builtins.property
    @jsii.member(jsii_name="continentInput")
    def continent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "continentInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="subdivisionInput")
    def subdivision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdivisionInput"))

    @builtins.property
    @jsii.member(jsii_name="continent")
    def continent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "continent"))

    @continent.setter
    def continent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eac6c06b7344f6603876e961a1b407767c1ef7f9c78cca73a07cb7d2f4b06e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continent", value)

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b23ad8d8fe6c473fe4a4c6711de07351bdf6bd695e9d521ff7308849b57179d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value)

    @builtins.property
    @jsii.member(jsii_name="subdivision")
    def subdivision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subdivision"))

    @subdivision.setter
    def subdivision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d7048941ef37128e015ef234e7e3f7d7a10f039c25eb0d6e79abdd0fdca32c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdivision", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[Route53RecordGeolocationRoutingPolicy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[Route53RecordGeolocationRoutingPolicy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[Route53RecordGeolocationRoutingPolicy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d802ffd32937b62f4b7f88ce9bf93f92a6eef45d4652babd81f8ca918d16c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordLatencyRoutingPolicy",
    jsii_struct_bases=[],
    name_mapping={"region": "region"},
)
class Route53RecordLatencyRoutingPolicy:
    def __init__(self, *, region: builtins.str) -> None:
        '''
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#region Route53Record#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93407d6d78c0b77af3feea7161e9af605afe9e663fb253ef2ef1ca1503a59584)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region": region,
        }

    @builtins.property
    def region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#region Route53Record#region}.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53RecordLatencyRoutingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53RecordLatencyRoutingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordLatencyRoutingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79400b6be59bc41169818fea6a36025a7f4c3df4b0a50dc5a88aba1f49b1defc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Route53RecordLatencyRoutingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc85f98ded96fda865e516c1d9093dbe7e4d5a200753c4c17c7a1a53e703642)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Route53RecordLatencyRoutingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e31c849a4a3025c1cd24307d66b6b5a03182f67fcfbd3ddff0f613eb9c6d9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4578e520b09cafeeb69b4253f9b788fe6516109dfd63d2e347da5f2792296b94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93bd9c0f4da3f7b683bea475c658e74f2006bab57da1b087b6438c07b7ef4f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordLatencyRoutingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordLatencyRoutingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordLatencyRoutingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bca09cef22639c5744dbbdbadaa710ae4ee71dabc30a33f666b2f3bf299342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class Route53RecordLatencyRoutingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordLatencyRoutingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba3cd52b8292c2ba519f8f806b7839e6b27393af20d8b65d7a64670fcddf0ad2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8378afccd68ee9cb4c0785f13812c5617e4ed27fb751af42d887586852e04a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[Route53RecordLatencyRoutingPolicy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[Route53RecordLatencyRoutingPolicy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[Route53RecordLatencyRoutingPolicy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd13bb47bb07a2a8f5498ebf74d6311512321696d47434bc0e655411c0502fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordWeightedRoutingPolicy",
    jsii_struct_bases=[],
    name_mapping={"weight": "weight"},
)
class Route53RecordWeightedRoutingPolicy:
    def __init__(self, *, weight: jsii.Number) -> None:
        '''
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#weight Route53Record#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83b655b37b076e5c3f4c03bb57e015b3849de49ef591587f99466c5249f0bcd)
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "weight": weight,
        }

    @builtins.property
    def weight(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/route53_record#weight Route53Record#weight}.'''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53RecordWeightedRoutingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53RecordWeightedRoutingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordWeightedRoutingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a8957df8ef6708d7419d158a53b470abb9cb44a636f43e55d24260c1bd040d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Route53RecordWeightedRoutingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43d955b2a1fea86f7acebf9928033374446cd20faa297821936985fbfa6f945)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Route53RecordWeightedRoutingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989df05cba562772ae162fcb26a00915ce859bacb627bf1573f63fdc26dd5aef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fec5463efca1ab97dbc18ddb2ba3025c42346a88fabddfe43cc1f43e922657bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b244b76d573fbd2c0aefb899869c53224ad3fe6a2e4c56aa539cd9b872b1a7d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordWeightedRoutingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordWeightedRoutingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordWeightedRoutingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066601c56c097d3c24e6aabe08534e93554e628dd71412faec51afb0df974a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class Route53RecordWeightedRoutingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53Record.Route53RecordWeightedRoutingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a322cbee89fad14284b2aab1c61c268f1eec35244785e5be924fe4b717a4f999)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e6911bd7492b91ddd6de3d8919e1b7b46b7162434ba30cb58eed1b77787280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[Route53RecordWeightedRoutingPolicy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[Route53RecordWeightedRoutingPolicy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[Route53RecordWeightedRoutingPolicy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d97afbd26b44ba4c734781314289d7fd1b200f949a004774faf3eda0fb1b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Route53Record",
    "Route53RecordAlias",
    "Route53RecordAliasList",
    "Route53RecordAliasOutputReference",
    "Route53RecordConfig",
    "Route53RecordFailoverRoutingPolicy",
    "Route53RecordFailoverRoutingPolicyList",
    "Route53RecordFailoverRoutingPolicyOutputReference",
    "Route53RecordGeolocationRoutingPolicy",
    "Route53RecordGeolocationRoutingPolicyList",
    "Route53RecordGeolocationRoutingPolicyOutputReference",
    "Route53RecordLatencyRoutingPolicy",
    "Route53RecordLatencyRoutingPolicyList",
    "Route53RecordLatencyRoutingPolicyOutputReference",
    "Route53RecordWeightedRoutingPolicy",
    "Route53RecordWeightedRoutingPolicyList",
    "Route53RecordWeightedRoutingPolicyOutputReference",
]

publication.publish()

def _typecheckingstub__10f5b59686cb8993858d6d7b9d56fb53382192067cad2c01362d14ebaaaec159(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    zone_id: builtins.str,
    alias: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordAlias, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allow_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failover_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordFailoverRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    geolocation_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordGeolocationRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health_check_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    latency_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordLatencyRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    multivalue_answer_routing_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    records: typing.Optional[typing.Sequence[builtins.str]] = None,
    set_identifier: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
    weighted_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordWeightedRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__2739e121e7c9f7d2b606d3e41d5c6bb67761d240bcd585c19f559c6e7b89178d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordAlias, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a7e6d94ecc1e0e93cb4ab10dde2a0536ab7d8a6a8274dfb5a2cce4702e9196(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordFailoverRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8410655fccd5114e61473d2de25656c368919e9ba62bf876bfa558659ea1018(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordGeolocationRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecb8be5f80e5732495d4ccc8f0a60874d3a9ead0f8e1f79e6a60682890aaf99(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordLatencyRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de79ba6bae13ff08c95efdc70144fafeaf57314e9e456db382e400597a7fd849(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordWeightedRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e822ce13c0c1f2e6ef47533cdceac5bfebf68ff7a84983a23ce3142acff7692(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5153b07b556a8e4336b215a9ba774b26a360439749b4337716c51c08dcde9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c46a03e80f09759a3049111f9214bf31cf381fed6e82f241daa93db2a96dbb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ecdf8a17309c19c46d4597e276e1a5d83bce2ffaea7ddf4ebaa98f4cdd933a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f69796a27e7ae2954e5965d462a7b6f58c32b03353caa20e077c603d983ace(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cfb6d133f3c765dbb87b21ce121c5a32f64e35564ad68c03fd612cb816a0bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e4edbcc53ac0eb95a961a293ef2f1f3a7dcecdb147f1cd8c602851748d78a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4774f1276093a280f9a33c1b88caadae84b4cf48d49f52399845c07a58a711c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b5957ba08d59ec45d652bff2891ef182ee4567633239591697615016fb2af4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6efc358fb10951b3d3f705725c430cf900d1c59597b44f689f99ccbd2e6df63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ad3458a72faf84e447106807b17f77177e205dcbf6498b3b7d74ee4c28b6d6(
    *,
    evaluate_target_health: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    zone_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c330e65508bfb3fe36ea6c3b9eace58ad220a72a5f5617001100a95512ced9a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8efd785bb1e39ee786671457bcccfc24b92fdcacff0366a4222779161519c6a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1abc1fb8420e3f04f233070f9486efee72dad232a0839ff3d714be480cb97a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbba7b694900fbb5a30db495a965d776387fa8d3810c3e2582c4d7d7b6841f3a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c448a1ea8bdb4bcec68dccffd450cbb3e64d16e0012bca0d32448cbfda55ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d6a6c861af2a6998f957034aa71f9dd2eb0b4b3f070e5784e10ca7276468af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordAlias]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2362a0284f0d13d848404a01d5524e028c28a3fb4c1dfed5ccb7e4ab40dd8511(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9828de0792ad65f7b056035a7f17abd8dbfed011972bb68f39c73d282dc335f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3069dca3a23be24e3e1ad2455a847bcf6a73229a610344df23a45cc98d4e665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2f575aac87161cfd818203c422e61dd24c064cea63eafc1e9c884327b2996c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042c8287bf7bc43b15d5320b876fa8bfa486458002db5dc11567d82fe956f751(
    value: typing.Optional[typing.Union[Route53RecordAlias, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1842bebe04831c413fc865c1760274061405c09f54bcf3093b64252b4cd4baad(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    type: builtins.str,
    zone_id: builtins.str,
    alias: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordAlias, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allow_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failover_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordFailoverRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    geolocation_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordGeolocationRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health_check_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    latency_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordLatencyRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    multivalue_answer_routing_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    records: typing.Optional[typing.Sequence[builtins.str]] = None,
    set_identifier: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
    weighted_routing_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53RecordWeightedRoutingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce0183eff110b972fee5a66acf0258247d1029d0f2a719bf041bb22d7f900bc(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4b68ebd030e48b5e9b5d807510f980514f53fa06d7f21c0d10a1bde7b9b92f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b3c0769945812f977d9c97959df7d4a24339e96bf5e3b4b0c56fe3d13add99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f70c1dc3989de544c993b5661f04b07e92119a3445a366629390ba40ecf2b7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03fd3f47102053e9f49cab8e674d38503c7b35e1c4d3fbbff3279080be0fedc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cd63b34d64e272ea5e8b1cdeaf0e8217600e35e37256c71f50c38e188adced(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9310c7823a8b1c6f3b93d7d460a454443103d038e675be8d5f0733e943cac051(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordFailoverRoutingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc079ac9358a23334e259a945ac81122d8583217d2dc10a8a73f8e3a0dbc097(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894be4fefe07e574ad08fcff21f9996be1b2319991c5c03cfe4cba33e64c6926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324ce71ecd0de1538bf9491d47f3ae9bfe952378173963353ee0ad633066898e(
    value: typing.Optional[typing.Union[Route53RecordFailoverRoutingPolicy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6b879ebb9bb510894d0f3fd3daa9a59d5c73af6a5a1e92636c597f68c25981(
    *,
    continent: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    subdivision: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b63c1516a16b05a941000bb1485db715638a3ce1996ccb96ce1ce9bde79159(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fb9a80d129007b7e99fa6c4eef4b9948ddc479d698f2668029a18433733621(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72a8e493d5cbb9966f28295e5a155e14ac1158b55aa67f83a463dab23093011(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3882a4abb54c93685ebf22c0cf5e3234dbbc6d43543d3a865e2436f3605ac8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad1a6eea3062048d0cd2133d2a6cf16c810c0d9ab27633b1ba290d0e15e9bac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d42a4169deb5ff0f78c6f6f08dcb61354da572c3a8b2adab77a9dcf451164c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordGeolocationRoutingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a7d46d635871cb83cb285ca11cc163e9070c04923b7313127c60b086f8bf0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eac6c06b7344f6603876e961a1b407767c1ef7f9c78cca73a07cb7d2f4b06e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b23ad8d8fe6c473fe4a4c6711de07351bdf6bd695e9d521ff7308849b57179d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d7048941ef37128e015ef234e7e3f7d7a10f039c25eb0d6e79abdd0fdca32c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d802ffd32937b62f4b7f88ce9bf93f92a6eef45d4652babd81f8ca918d16c8(
    value: typing.Optional[typing.Union[Route53RecordGeolocationRoutingPolicy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93407d6d78c0b77af3feea7161e9af605afe9e663fb253ef2ef1ca1503a59584(
    *,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79400b6be59bc41169818fea6a36025a7f4c3df4b0a50dc5a88aba1f49b1defc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc85f98ded96fda865e516c1d9093dbe7e4d5a200753c4c17c7a1a53e703642(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e31c849a4a3025c1cd24307d66b6b5a03182f67fcfbd3ddff0f613eb9c6d9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4578e520b09cafeeb69b4253f9b788fe6516109dfd63d2e347da5f2792296b94(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93bd9c0f4da3f7b683bea475c658e74f2006bab57da1b087b6438c07b7ef4f62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bca09cef22639c5744dbbdbadaa710ae4ee71dabc30a33f666b2f3bf299342(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordLatencyRoutingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3cd52b8292c2ba519f8f806b7839e6b27393af20d8b65d7a64670fcddf0ad2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8378afccd68ee9cb4c0785f13812c5617e4ed27fb751af42d887586852e04a2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd13bb47bb07a2a8f5498ebf74d6311512321696d47434bc0e655411c0502fa(
    value: typing.Optional[typing.Union[Route53RecordLatencyRoutingPolicy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83b655b37b076e5c3f4c03bb57e015b3849de49ef591587f99466c5249f0bcd(
    *,
    weight: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a8957df8ef6708d7419d158a53b470abb9cb44a636f43e55d24260c1bd040d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43d955b2a1fea86f7acebf9928033374446cd20faa297821936985fbfa6f945(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989df05cba562772ae162fcb26a00915ce859bacb627bf1573f63fdc26dd5aef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec5463efca1ab97dbc18ddb2ba3025c42346a88fabddfe43cc1f43e922657bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b244b76d573fbd2c0aefb899869c53224ad3fe6a2e4c56aa539cd9b872b1a7d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066601c56c097d3c24e6aabe08534e93554e628dd71412faec51afb0df974a6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53RecordWeightedRoutingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a322cbee89fad14284b2aab1c61c268f1eec35244785e5be924fe4b717a4f999(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e6911bd7492b91ddd6de3d8919e1b7b46b7162434ba30cb58eed1b77787280(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d97afbd26b44ba4c734781314289d7fd1b200f949a004774faf3eda0fb1b8d(
    value: typing.Optional[typing.Union[Route53RecordWeightedRoutingPolicy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
