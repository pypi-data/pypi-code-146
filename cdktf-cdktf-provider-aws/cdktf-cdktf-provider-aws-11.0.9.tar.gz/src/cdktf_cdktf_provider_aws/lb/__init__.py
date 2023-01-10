'''
# `aws_lb`

Refer to the Terraform Registory for docs: [`aws_lb`](https://www.terraform.io/docs/providers/aws/r/lb).
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


class Lb(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lb.Lb",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/lb aws_lb}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_logs: typing.Optional[typing.Union["LbAccessLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
        desync_mitigation_mode: typing.Optional[builtins.str] = None,
        drop_invalid_header_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_cross_zone_load_balancing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_waf_fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_timeout: typing.Optional[jsii.Number] = None,
        internal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        load_balancer_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        preserve_host_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbSubnetMapping", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LbTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/lb aws_lb} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_logs: access_logs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#access_logs Lb#access_logs}
        :param customer_owned_ipv4_pool: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#customer_owned_ipv4_pool Lb#customer_owned_ipv4_pool}.
        :param desync_mitigation_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#desync_mitigation_mode Lb#desync_mitigation_mode}.
        :param drop_invalid_header_fields: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#drop_invalid_header_fields Lb#drop_invalid_header_fields}.
        :param enable_cross_zone_load_balancing: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_cross_zone_load_balancing Lb#enable_cross_zone_load_balancing}.
        :param enable_deletion_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_deletion_protection Lb#enable_deletion_protection}.
        :param enable_http2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_http2 Lb#enable_http2}.
        :param enable_waf_fail_open: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_waf_fail_open Lb#enable_waf_fail_open}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#id Lb#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#idle_timeout Lb#idle_timeout}.
        :param internal: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#internal Lb#internal}.
        :param ip_address_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#ip_address_type Lb#ip_address_type}.
        :param load_balancer_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#load_balancer_type Lb#load_balancer_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#name Lb#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#name_prefix Lb#name_prefix}.
        :param preserve_host_header: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#preserve_host_header Lb#preserve_host_header}.
        :param security_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#security_groups Lb#security_groups}.
        :param subnet_mapping: subnet_mapping block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#subnet_mapping Lb#subnet_mapping}
        :param subnets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#subnets Lb#subnets}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#tags Lb#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#tags_all Lb#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#timeouts Lb#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e908418abdfb0361ed1b24ed1ce275f361352462ef304e91db52683225c27458)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LbConfig(
            access_logs=access_logs,
            customer_owned_ipv4_pool=customer_owned_ipv4_pool,
            desync_mitigation_mode=desync_mitigation_mode,
            drop_invalid_header_fields=drop_invalid_header_fields,
            enable_cross_zone_load_balancing=enable_cross_zone_load_balancing,
            enable_deletion_protection=enable_deletion_protection,
            enable_http2=enable_http2,
            enable_waf_fail_open=enable_waf_fail_open,
            id=id,
            idle_timeout=idle_timeout,
            internal=internal,
            ip_address_type=ip_address_type,
            load_balancer_type=load_balancer_type,
            name=name,
            name_prefix=name_prefix,
            preserve_host_header=preserve_host_header,
            security_groups=security_groups,
            subnet_mapping=subnet_mapping,
            subnets=subnets,
            tags=tags,
            tags_all=tags_all,
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

    @jsii.member(jsii_name="putAccessLogs")
    def put_access_logs(
        self,
        *,
        bucket: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#bucket Lb#bucket}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enabled Lb#enabled}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#prefix Lb#prefix}.
        '''
        value = LbAccessLogs(bucket=bucket, enabled=enabled, prefix=prefix)

        return typing.cast(None, jsii.invoke(self, "putAccessLogs", [value]))

    @jsii.member(jsii_name="putSubnetMapping")
    def put_subnet_mapping(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbSubnetMapping", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40dff90a6c6a2e9be3bfc42787d617de1a3e48eee4f44f46b45b174abcf4a24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubnetMapping", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#create Lb#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#delete Lb#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#update Lb#update}.
        '''
        value = LbTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessLogs")
    def reset_access_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLogs", []))

    @jsii.member(jsii_name="resetCustomerOwnedIpv4Pool")
    def reset_customer_owned_ipv4_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerOwnedIpv4Pool", []))

    @jsii.member(jsii_name="resetDesyncMitigationMode")
    def reset_desync_mitigation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesyncMitigationMode", []))

    @jsii.member(jsii_name="resetDropInvalidHeaderFields")
    def reset_drop_invalid_header_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropInvalidHeaderFields", []))

    @jsii.member(jsii_name="resetEnableCrossZoneLoadBalancing")
    def reset_enable_cross_zone_load_balancing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableCrossZoneLoadBalancing", []))

    @jsii.member(jsii_name="resetEnableDeletionProtection")
    def reset_enable_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDeletionProtection", []))

    @jsii.member(jsii_name="resetEnableHttp2")
    def reset_enable_http2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHttp2", []))

    @jsii.member(jsii_name="resetEnableWafFailOpen")
    def reset_enable_waf_fail_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableWafFailOpen", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdleTimeout")
    def reset_idle_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeout", []))

    @jsii.member(jsii_name="resetInternal")
    def reset_internal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternal", []))

    @jsii.member(jsii_name="resetIpAddressType")
    def reset_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressType", []))

    @jsii.member(jsii_name="resetLoadBalancerType")
    def reset_load_balancer_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerType", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetPreserveHostHeader")
    def reset_preserve_host_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveHostHeader", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSubnetMapping")
    def reset_subnet_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetMapping", []))

    @jsii.member(jsii_name="resetSubnets")
    def reset_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnets", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="accessLogs")
    def access_logs(self) -> "LbAccessLogsOutputReference":
        return typing.cast("LbAccessLogsOutputReference", jsii.get(self, "accessLogs"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="arnSuffix")
    def arn_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arnSuffix"))

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @builtins.property
    @jsii.member(jsii_name="subnetMapping")
    def subnet_mapping(self) -> "LbSubnetMappingList":
        return typing.cast("LbSubnetMappingList", jsii.get(self, "subnetMapping"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LbTimeoutsOutputReference":
        return typing.cast("LbTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @builtins.property
    @jsii.member(jsii_name="accessLogsInput")
    def access_logs_input(self) -> typing.Optional["LbAccessLogs"]:
        return typing.cast(typing.Optional["LbAccessLogs"], jsii.get(self, "accessLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="customerOwnedIpv4PoolInput")
    def customer_owned_ipv4_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerOwnedIpv4PoolInput"))

    @builtins.property
    @jsii.member(jsii_name="desyncMitigationModeInput")
    def desync_mitigation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desyncMitigationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="dropInvalidHeaderFieldsInput")
    def drop_invalid_header_fields_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropInvalidHeaderFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableCrossZoneLoadBalancingInput")
    def enable_cross_zone_load_balancing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableCrossZoneLoadBalancingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDeletionProtectionInput")
    def enable_deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDeletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHttp2Input")
    def enable_http2_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHttp2Input"))

    @builtins.property
    @jsii.member(jsii_name="enableWafFailOpenInput")
    def enable_waf_fail_open_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableWafFailOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInput")
    def idle_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="internalInput")
    def internal_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressTypeInput")
    def ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveHostHeaderInput")
    def preserve_host_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveHostHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetMappingInput")
    def subnet_mapping_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbSubnetMapping"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbSubnetMapping"]]], jsii.get(self, "subnetMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["LbTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["LbTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="customerOwnedIpv4Pool")
    def customer_owned_ipv4_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerOwnedIpv4Pool"))

    @customer_owned_ipv4_pool.setter
    def customer_owned_ipv4_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb8a38b0a24ac16e1250314e74bb24b917530f16705bcebb2402b6b5e8260651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerOwnedIpv4Pool", value)

    @builtins.property
    @jsii.member(jsii_name="desyncMitigationMode")
    def desync_mitigation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desyncMitigationMode"))

    @desync_mitigation_mode.setter
    def desync_mitigation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f70aacd7990e73c7950d083a72a01f0f8f81d78a229749cb8f75fed38fe364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desyncMitigationMode", value)

    @builtins.property
    @jsii.member(jsii_name="dropInvalidHeaderFields")
    def drop_invalid_header_fields(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropInvalidHeaderFields"))

    @drop_invalid_header_fields.setter
    def drop_invalid_header_fields(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f919c4598f95685b9c147a7e51c12ecc231a63c9589c271bbd2827a6795a5c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropInvalidHeaderFields", value)

    @builtins.property
    @jsii.member(jsii_name="enableCrossZoneLoadBalancing")
    def enable_cross_zone_load_balancing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableCrossZoneLoadBalancing"))

    @enable_cross_zone_load_balancing.setter
    def enable_cross_zone_load_balancing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b6884a9373474a200b907ae77a696c22e4ecb08b6eadbb2748bc6b8571d914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCrossZoneLoadBalancing", value)

    @builtins.property
    @jsii.member(jsii_name="enableDeletionProtection")
    def enable_deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDeletionProtection"))

    @enable_deletion_protection.setter
    def enable_deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ffb06f088d85ef1d06376c73378aa081c5a7ecf224c2cf1e8936aa028626e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDeletionProtection", value)

    @builtins.property
    @jsii.member(jsii_name="enableHttp2")
    def enable_http2(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHttp2"))

    @enable_http2.setter
    def enable_http2(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ccb4a58bb8b9d6a3948ab327836612b907aaa0cce75bde611c4fcebb62d4a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHttp2", value)

    @builtins.property
    @jsii.member(jsii_name="enableWafFailOpen")
    def enable_waf_fail_open(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableWafFailOpen"))

    @enable_waf_fail_open.setter
    def enable_waf_fail_open(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74a5abbb7140a2fcbcfcde81f65c67b465a5d3bba90a209f2e423751b3ac681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableWafFailOpen", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e425911ed780ca0aa006d5832a484b674fce4929ef3971f37e9b46ff2a8131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="idleTimeout")
    def idle_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleTimeout"))

    @idle_timeout.setter
    def idle_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da1d70b62a278d6bbd9fec39696f5c40fa3cccb062f713621a2366879e3e9ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="internal")
    def internal(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internal"))

    @internal.setter
    def internal(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8efd543331e8dc786a2cfbb6c82b0ee70efdf531f63b54aa81ebbac991ee648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internal", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53957ef43684a4a4c0b702ab04c00c3248702e007f4d350632be757075b1f39c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressType", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220c4c2f56f5ebfc51a8f74000aaf7cce92293e88232969a3662bf618767aa81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba8959b1279397df92882436a743973a6e1be73eab952bd80e34daf579313ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63909e2a3e67acb91bd2f217b61d6a1003eea1a3df7c09975532d24b05ca8c53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="preserveHostHeader")
    def preserve_host_header(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveHostHeader"))

    @preserve_host_header.setter
    def preserve_host_header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fba678cefd8ce92a0a242fcfa176851d8334940d1310e4e8ae5f9430e6da04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveHostHeader", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4251992bb92158db861524624e3d0bdc779e2b8e6433a61f77b0385d6f021a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8194e168e149985abcecedcbcc56288d60022ae8943ba8357a22caa85a16fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733b52be7cf1fc8ae57ab3d4fb4d23fda5ebd5c7a728a7953994d1eb0d74dbea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947268b5257783b55317506c69d290612e132e7d1d256668798c3cb0855fa7ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lb.LbAccessLogs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "enabled": "enabled", "prefix": "prefix"},
)
class LbAccessLogs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#bucket Lb#bucket}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enabled Lb#enabled}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#prefix Lb#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9420a9b0852475d53a14a56107412fbed8fe9f6d0b19f3388dff688e494337)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#bucket Lb#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enabled Lb#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#prefix Lb#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbAccessLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbAccessLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lb.LbAccessLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b83abb1871b7f95f96f775eec60fcb7fa5ec8c9ed15af6b666aaaeb195088bce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8868cbccc11da3816985f8685ff489a4e1ae96a6413092e2133c659cabdf706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19eeb87159bf92021326c98cd18416104b39ceffd38700ff171b9db7c74cb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376cebd6ca780d4197eff8b0ba16cf4b9279cc6935863516b1527437cf5bc102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbAccessLogs]:
        return typing.cast(typing.Optional[LbAccessLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LbAccessLogs]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd256a30b2f725348183853d303de574d59375265580d45306c8844a83178c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lb.LbConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_logs": "accessLogs",
        "customer_owned_ipv4_pool": "customerOwnedIpv4Pool",
        "desync_mitigation_mode": "desyncMitigationMode",
        "drop_invalid_header_fields": "dropInvalidHeaderFields",
        "enable_cross_zone_load_balancing": "enableCrossZoneLoadBalancing",
        "enable_deletion_protection": "enableDeletionProtection",
        "enable_http2": "enableHttp2",
        "enable_waf_fail_open": "enableWafFailOpen",
        "id": "id",
        "idle_timeout": "idleTimeout",
        "internal": "internal",
        "ip_address_type": "ipAddressType",
        "load_balancer_type": "loadBalancerType",
        "name": "name",
        "name_prefix": "namePrefix",
        "preserve_host_header": "preserveHostHeader",
        "security_groups": "securityGroups",
        "subnet_mapping": "subnetMapping",
        "subnets": "subnets",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class LbConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_logs: typing.Optional[typing.Union[LbAccessLogs, typing.Dict[builtins.str, typing.Any]]] = None,
        customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
        desync_mitigation_mode: typing.Optional[builtins.str] = None,
        drop_invalid_header_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_cross_zone_load_balancing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_waf_fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_timeout: typing.Optional[jsii.Number] = None,
        internal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        load_balancer_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        preserve_host_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbSubnetMapping", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LbTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_logs: access_logs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#access_logs Lb#access_logs}
        :param customer_owned_ipv4_pool: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#customer_owned_ipv4_pool Lb#customer_owned_ipv4_pool}.
        :param desync_mitigation_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#desync_mitigation_mode Lb#desync_mitigation_mode}.
        :param drop_invalid_header_fields: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#drop_invalid_header_fields Lb#drop_invalid_header_fields}.
        :param enable_cross_zone_load_balancing: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_cross_zone_load_balancing Lb#enable_cross_zone_load_balancing}.
        :param enable_deletion_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_deletion_protection Lb#enable_deletion_protection}.
        :param enable_http2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_http2 Lb#enable_http2}.
        :param enable_waf_fail_open: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_waf_fail_open Lb#enable_waf_fail_open}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#id Lb#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#idle_timeout Lb#idle_timeout}.
        :param internal: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#internal Lb#internal}.
        :param ip_address_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#ip_address_type Lb#ip_address_type}.
        :param load_balancer_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#load_balancer_type Lb#load_balancer_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#name Lb#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#name_prefix Lb#name_prefix}.
        :param preserve_host_header: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#preserve_host_header Lb#preserve_host_header}.
        :param security_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#security_groups Lb#security_groups}.
        :param subnet_mapping: subnet_mapping block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#subnet_mapping Lb#subnet_mapping}
        :param subnets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#subnets Lb#subnets}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#tags Lb#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#tags_all Lb#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#timeouts Lb#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_logs, dict):
            access_logs = LbAccessLogs(**access_logs)
        if isinstance(timeouts, dict):
            timeouts = LbTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d514c61a23aef8e4b8786d77e3d924b68c850ff0e610f94a30a1878d353664b4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_logs", value=access_logs, expected_type=type_hints["access_logs"])
            check_type(argname="argument customer_owned_ipv4_pool", value=customer_owned_ipv4_pool, expected_type=type_hints["customer_owned_ipv4_pool"])
            check_type(argname="argument desync_mitigation_mode", value=desync_mitigation_mode, expected_type=type_hints["desync_mitigation_mode"])
            check_type(argname="argument drop_invalid_header_fields", value=drop_invalid_header_fields, expected_type=type_hints["drop_invalid_header_fields"])
            check_type(argname="argument enable_cross_zone_load_balancing", value=enable_cross_zone_load_balancing, expected_type=type_hints["enable_cross_zone_load_balancing"])
            check_type(argname="argument enable_deletion_protection", value=enable_deletion_protection, expected_type=type_hints["enable_deletion_protection"])
            check_type(argname="argument enable_http2", value=enable_http2, expected_type=type_hints["enable_http2"])
            check_type(argname="argument enable_waf_fail_open", value=enable_waf_fail_open, expected_type=type_hints["enable_waf_fail_open"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
            check_type(argname="argument internal", value=internal, expected_type=type_hints["internal"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument preserve_host_header", value=preserve_host_header, expected_type=type_hints["preserve_host_header"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_mapping", value=subnet_mapping, expected_type=type_hints["subnet_mapping"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
        if access_logs is not None:
            self._values["access_logs"] = access_logs
        if customer_owned_ipv4_pool is not None:
            self._values["customer_owned_ipv4_pool"] = customer_owned_ipv4_pool
        if desync_mitigation_mode is not None:
            self._values["desync_mitigation_mode"] = desync_mitigation_mode
        if drop_invalid_header_fields is not None:
            self._values["drop_invalid_header_fields"] = drop_invalid_header_fields
        if enable_cross_zone_load_balancing is not None:
            self._values["enable_cross_zone_load_balancing"] = enable_cross_zone_load_balancing
        if enable_deletion_protection is not None:
            self._values["enable_deletion_protection"] = enable_deletion_protection
        if enable_http2 is not None:
            self._values["enable_http2"] = enable_http2
        if enable_waf_fail_open is not None:
            self._values["enable_waf_fail_open"] = enable_waf_fail_open
        if id is not None:
            self._values["id"] = id
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout
        if internal is not None:
            self._values["internal"] = internal
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if load_balancer_type is not None:
            self._values["load_balancer_type"] = load_balancer_type
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if preserve_host_header is not None:
            self._values["preserve_host_header"] = preserve_host_header
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_mapping is not None:
            self._values["subnet_mapping"] = subnet_mapping
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
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
    def access_logs(self) -> typing.Optional[LbAccessLogs]:
        '''access_logs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#access_logs Lb#access_logs}
        '''
        result = self._values.get("access_logs")
        return typing.cast(typing.Optional[LbAccessLogs], result)

    @builtins.property
    def customer_owned_ipv4_pool(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#customer_owned_ipv4_pool Lb#customer_owned_ipv4_pool}.'''
        result = self._values.get("customer_owned_ipv4_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desync_mitigation_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#desync_mitigation_mode Lb#desync_mitigation_mode}.'''
        result = self._values.get("desync_mitigation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def drop_invalid_header_fields(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#drop_invalid_header_fields Lb#drop_invalid_header_fields}.'''
        result = self._values.get("drop_invalid_header_fields")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_cross_zone_load_balancing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_cross_zone_load_balancing Lb#enable_cross_zone_load_balancing}.'''
        result = self._values.get("enable_cross_zone_load_balancing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_deletion_protection Lb#enable_deletion_protection}.'''
        result = self._values.get("enable_deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_http2(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_http2 Lb#enable_http2}.'''
        result = self._values.get("enable_http2")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_waf_fail_open(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#enable_waf_fail_open Lb#enable_waf_fail_open}.'''
        result = self._values.get("enable_waf_fail_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#id Lb#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#idle_timeout Lb#idle_timeout}.'''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def internal(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#internal Lb#internal}.'''
        result = self._values.get("internal")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#ip_address_type Lb#ip_address_type}.'''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#load_balancer_type Lb#load_balancer_type}.'''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#name Lb#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#name_prefix Lb#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_host_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#preserve_host_header Lb#preserve_host_header}.'''
        result = self._values.get("preserve_host_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#security_groups Lb#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_mapping(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbSubnetMapping"]]]:
        '''subnet_mapping block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#subnet_mapping Lb#subnet_mapping}
        '''
        result = self._values.get("subnet_mapping")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbSubnetMapping"]]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#subnets Lb#subnets}.'''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#tags Lb#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#tags_all Lb#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LbTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#timeouts Lb#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LbTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lb.LbSubnetMapping",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_id": "subnetId",
        "allocation_id": "allocationId",
        "ipv6_address": "ipv6Address",
        "private_ipv4_address": "privateIpv4Address",
    },
)
class LbSubnetMapping:
    def __init__(
        self,
        *,
        subnet_id: builtins.str,
        allocation_id: typing.Optional[builtins.str] = None,
        ipv6_address: typing.Optional[builtins.str] = None,
        private_ipv4_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#subnet_id Lb#subnet_id}.
        :param allocation_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#allocation_id Lb#allocation_id}.
        :param ipv6_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#ipv6_address Lb#ipv6_address}.
        :param private_ipv4_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#private_ipv4_address Lb#private_ipv4_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa10a32ce162c3a969945a8abaeb000051efdbaa9316190b230bd0586f35e4c)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument allocation_id", value=allocation_id, expected_type=type_hints["allocation_id"])
            check_type(argname="argument ipv6_address", value=ipv6_address, expected_type=type_hints["ipv6_address"])
            check_type(argname="argument private_ipv4_address", value=private_ipv4_address, expected_type=type_hints["private_ipv4_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
        }
        if allocation_id is not None:
            self._values["allocation_id"] = allocation_id
        if ipv6_address is not None:
            self._values["ipv6_address"] = ipv6_address
        if private_ipv4_address is not None:
            self._values["private_ipv4_address"] = private_ipv4_address

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#subnet_id Lb#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allocation_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#allocation_id Lb#allocation_id}.'''
        result = self._values.get("allocation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#ipv6_address Lb#ipv6_address}.'''
        result = self._values.get("ipv6_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ipv4_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#private_ipv4_address Lb#private_ipv4_address}.'''
        result = self._values.get("private_ipv4_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbSubnetMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbSubnetMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lb.LbSubnetMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9fc9da707f6bf5ff8a071978c04ae2b1496cb251035b3ed651da396a3eab2e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LbSubnetMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84383dea5592c3921654dd387e56f1e3d6a5021fcd8a7d9f07e576055bbe0cac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LbSubnetMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83fc579d3748b3fe7123f2ae13aa026546089c4a7370b8224d4b56099d011b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06a118b58c60ed6fe3f84ceacdec15cbebfaa7b6cd8f7bca833f9b613034d8d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bb63cc4fc558334bce6b386bd9a2b41cf18307279caca54ec7e84536d122062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbSubnetMapping]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbSubnetMapping]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbSubnetMapping]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb41a94b3ebe3dd537ed54ead4f3868f8c7ab1512b7607c3ab307b51f8ebd750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LbSubnetMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lb.LbSubnetMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6afe4b5df729653f3d4a770b83e0830a0bd304a368f8c300a7c1d562f1a18e58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllocationId")
    def reset_allocation_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocationId", []))

    @jsii.member(jsii_name="resetIpv6Address")
    def reset_ipv6_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Address", []))

    @jsii.member(jsii_name="resetPrivateIpv4Address")
    def reset_private_ipv4_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpv4Address", []))

    @builtins.property
    @jsii.member(jsii_name="outpostId")
    def outpost_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outpostId"))

    @builtins.property
    @jsii.member(jsii_name="allocationIdInput")
    def allocation_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AddressInput")
    def ipv6_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpv4AddressInput")
    def private_ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allocationId")
    def allocation_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocationId"))

    @allocation_id.setter
    def allocation_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2019c8c83e4faba5f50f1e6a0dc7b18300b47ba2129e547b9c15b969fc6a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocationId", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6Address")
    def ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Address"))

    @ipv6_address.setter
    def ipv6_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7143632185594355189f5436d65aa8cbb93dac04c395ecf9fec10ff866147bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Address", value)

    @builtins.property
    @jsii.member(jsii_name="privateIpv4Address")
    def private_ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpv4Address"))

    @private_ipv4_address.setter
    def private_ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ada448f3fd4c5d54070d686f6626160d25a4623fd0dc9c89c5dd1a86016ed21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpv4Address", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37bfff8473706f4fd7579dc7e930a0968444a54e5b86866745de628aac85960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LbSubnetMapping, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LbSubnetMapping, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LbSubnetMapping, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c13fb8d1e1adc12d8e5bc106668e00a5b687d5ee84c5967c928e2d383cb124c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lb.LbTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class LbTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#create Lb#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#delete Lb#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#update Lb#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31da6f853b27ebeaf02360aca1e13581fda0da5bda10ffb5a0535ca0d7b8887f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#create Lb#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#delete Lb#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lb#update Lb#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lb.LbTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__683b513f0eaaa83de561d85df51490545f4721a07d423b74148b3dbf19134ace)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff83dc121f18970815be9c499a9621aa271691170a94a575e4c573006c6549c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac3c3abae7f97ceb7164d138347fa953ec1fbdc519cd33004e51993b845ea23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f71a32cae7526d7e9c7eaab2b80e88121fdf7c112c4fc2a96a4353542ecee79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LbTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LbTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LbTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ebde1f6bb2674d6d5870beb139ddebfa51e152d6021c0e71a62ab70d4ae9e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Lb",
    "LbAccessLogs",
    "LbAccessLogsOutputReference",
    "LbConfig",
    "LbSubnetMapping",
    "LbSubnetMappingList",
    "LbSubnetMappingOutputReference",
    "LbTimeouts",
    "LbTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e908418abdfb0361ed1b24ed1ce275f361352462ef304e91db52683225c27458(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_logs: typing.Optional[typing.Union[LbAccessLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
    desync_mitigation_mode: typing.Optional[builtins.str] = None,
    drop_invalid_header_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_cross_zone_load_balancing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_waf_fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[jsii.Number] = None,
    internal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    load_balancer_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    preserve_host_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbSubnetMapping, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LbTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__40dff90a6c6a2e9be3bfc42787d617de1a3e48eee4f44f46b45b174abcf4a24e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbSubnetMapping, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8a38b0a24ac16e1250314e74bb24b917530f16705bcebb2402b6b5e8260651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f70aacd7990e73c7950d083a72a01f0f8f81d78a229749cb8f75fed38fe364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f919c4598f95685b9c147a7e51c12ecc231a63c9589c271bbd2827a6795a5c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b6884a9373474a200b907ae77a696c22e4ecb08b6eadbb2748bc6b8571d914(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffb06f088d85ef1d06376c73378aa081c5a7ecf224c2cf1e8936aa028626e17(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ccb4a58bb8b9d6a3948ab327836612b907aaa0cce75bde611c4fcebb62d4a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74a5abbb7140a2fcbcfcde81f65c67b465a5d3bba90a209f2e423751b3ac681(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e425911ed780ca0aa006d5832a484b674fce4929ef3971f37e9b46ff2a8131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da1d70b62a278d6bbd9fec39696f5c40fa3cccb062f713621a2366879e3e9ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8efd543331e8dc786a2cfbb6c82b0ee70efdf531f63b54aa81ebbac991ee648(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53957ef43684a4a4c0b702ab04c00c3248702e007f4d350632be757075b1f39c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220c4c2f56f5ebfc51a8f74000aaf7cce92293e88232969a3662bf618767aa81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba8959b1279397df92882436a743973a6e1be73eab952bd80e34daf579313ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63909e2a3e67acb91bd2f217b61d6a1003eea1a3df7c09975532d24b05ca8c53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fba678cefd8ce92a0a242fcfa176851d8334940d1310e4e8ae5f9430e6da04(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4251992bb92158db861524624e3d0bdc779e2b8e6433a61f77b0385d6f021a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8194e168e149985abcecedcbcc56288d60022ae8943ba8357a22caa85a16fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733b52be7cf1fc8ae57ab3d4fb4d23fda5ebd5c7a728a7953994d1eb0d74dbea(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947268b5257783b55317506c69d290612e132e7d1d256668798c3cb0855fa7ca(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9420a9b0852475d53a14a56107412fbed8fe9f6d0b19f3388dff688e494337(
    *,
    bucket: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83abb1871b7f95f96f775eec60fcb7fa5ec8c9ed15af6b666aaaeb195088bce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8868cbccc11da3816985f8685ff489a4e1ae96a6413092e2133c659cabdf706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19eeb87159bf92021326c98cd18416104b39ceffd38700ff171b9db7c74cb3b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376cebd6ca780d4197eff8b0ba16cf4b9279cc6935863516b1527437cf5bc102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd256a30b2f725348183853d303de574d59375265580d45306c8844a83178c60(
    value: typing.Optional[LbAccessLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d514c61a23aef8e4b8786d77e3d924b68c850ff0e610f94a30a1878d353664b4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_logs: typing.Optional[typing.Union[LbAccessLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
    desync_mitigation_mode: typing.Optional[builtins.str] = None,
    drop_invalid_header_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_cross_zone_load_balancing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_waf_fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[jsii.Number] = None,
    internal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    load_balancer_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    preserve_host_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbSubnetMapping, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LbTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa10a32ce162c3a969945a8abaeb000051efdbaa9316190b230bd0586f35e4c(
    *,
    subnet_id: builtins.str,
    allocation_id: typing.Optional[builtins.str] = None,
    ipv6_address: typing.Optional[builtins.str] = None,
    private_ipv4_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9fc9da707f6bf5ff8a071978c04ae2b1496cb251035b3ed651da396a3eab2e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84383dea5592c3921654dd387e56f1e3d6a5021fcd8a7d9f07e576055bbe0cac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83fc579d3748b3fe7123f2ae13aa026546089c4a7370b8224d4b56099d011b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a118b58c60ed6fe3f84ceacdec15cbebfaa7b6cd8f7bca833f9b613034d8d3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb63cc4fc558334bce6b386bd9a2b41cf18307279caca54ec7e84536d122062(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb41a94b3ebe3dd537ed54ead4f3868f8c7ab1512b7607c3ab307b51f8ebd750(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbSubnetMapping]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afe4b5df729653f3d4a770b83e0830a0bd304a368f8c300a7c1d562f1a18e58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2019c8c83e4faba5f50f1e6a0dc7b18300b47ba2129e547b9c15b969fc6a73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7143632185594355189f5436d65aa8cbb93dac04c395ecf9fec10ff866147bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ada448f3fd4c5d54070d686f6626160d25a4623fd0dc9c89c5dd1a86016ed21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37bfff8473706f4fd7579dc7e930a0968444a54e5b86866745de628aac85960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c13fb8d1e1adc12d8e5bc106668e00a5b687d5ee84c5967c928e2d383cb124c(
    value: typing.Optional[typing.Union[LbSubnetMapping, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31da6f853b27ebeaf02360aca1e13581fda0da5bda10ffb5a0535ca0d7b8887f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683b513f0eaaa83de561d85df51490545f4721a07d423b74148b3dbf19134ace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff83dc121f18970815be9c499a9621aa271691170a94a575e4c573006c6549c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac3c3abae7f97ceb7164d138347fa953ec1fbdc519cd33004e51993b845ea23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f71a32cae7526d7e9c7eaab2b80e88121fdf7c112c4fc2a96a4353542ecee79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ebde1f6bb2674d6d5870beb139ddebfa51e152d6021c0e71a62ab70d4ae9e0(
    value: typing.Optional[typing.Union[LbTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
