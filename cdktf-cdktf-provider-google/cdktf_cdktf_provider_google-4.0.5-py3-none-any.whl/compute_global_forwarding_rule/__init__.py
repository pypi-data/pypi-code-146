'''
# `google_compute_global_forwarding_rule`

Refer to the Terraform Registory for docs: [`google_compute_global_forwarding_rule`](https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule).
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


class ComputeGlobalForwardingRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule google_compute_global_forwarding_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[builtins.str] = None,
        port_range: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeGlobalForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule google_compute_global_forwarding_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression ``[a-z]([-a-z0-9]*[a-z0-9])?`` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must live in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. For ``INTERNAL_SELF_MANAGED`` load balancing, only ``targetHttpProxy`` is valid, not ``targetHttpsProxy``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#target ComputeGlobalForwardingRule#target}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#description ComputeGlobalForwardingRule#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#id ComputeGlobalForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address that this forwarding rule serves. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the target that you specify in the forwarding rule. If you don't specify a reserved IP address, an ephemeral IP address is assigned. Methods for specifying an IP address: * IPv4 dotted decimal, as in ``100.1.2.3`` * Full URL, as in ``https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name`` * Partial URL or by name, as in: * ``projects/project_id/regions/region/addresses/address-name`` * ``regions/region/addresses/address-name`` * ``global/addresses/address-name`` * ``address-name`` The loadBalancingScheme and the forwarding rule's target determine the type of IP address that you can use. For detailed information, refer to `IP address specifications </load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_address ComputeGlobalForwardingRule#ip_address}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are ``TCP``, ``UDP``, ``ESP``, ``AH``, ``SCTP`` or ``ICMP``. For Internal TCP/UDP Load Balancing, the load balancing scheme is ``INTERNAL``, and one of ``TCP`` or ``UDP`` are valid. For Traffic Director, the load balancing scheme is ``INTERNAL_SELF_MANAGED``, and only ``TCP``is valid. For Internal HTTP(S) Load Balancing, the load balancing scheme is ``INTERNAL_MANAGED``, and only ``TCP`` is valid. For HTTP(S), SSL Proxy, and TCP Proxy Load Balancing, the load balancing scheme is ``EXTERNAL`` and only ``TCP`` is valid. For Network TCP/UDP Load Balancing, the load balancing scheme is ``EXTERNAL``, and one of ``TCP`` or ``UDP`` is valid. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_protocol ComputeGlobalForwardingRule#ip_protocol}
        :param ip_version: The IP Version that will be used by this forwarding rule. Valid options are ``IPV4`` or ``IPV6``. This can only be specified for an external global forwarding rule. Possible values: UNSPECIFIED_VERSION, IPV4, IPV6 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_version ComputeGlobalForwardingRule#ip_version}
        :param labels: Labels to apply to this rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#labels ComputeGlobalForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. ``EXTERNAL`` is used for: Classic Cloud VPN gateways Protocol forwarding to VMs from an external IP address The following load balancers: HTTP(S), SSL Proxy, TCP Proxy, and Network TCP/UDP ``INTERNAL`` is used for: Protocol forwarding to VMs from an internal IP address Internal TCP/UDP load balancers ``INTERNAL_MANAGED`` is used for: Internal HTTP(S) load balancers ``INTERNAL_SELF_MANAGED`` is used for: Traffic Director ``EXTERNAL_MANAGED`` is used for: Global external HTTP(S) load balancers For more information about forwarding rules, refer to `Forwarding rule concepts </load-balancing/docs/forwarding-rule-concepts>`_. Possible values: INVALID, INTERNAL, INTERNAL_MANAGED, INTERNAL_SELF_MANAGED, EXTERNAL, EXTERNAL_MANAGED Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#load_balancing_scheme ComputeGlobalForwardingRule#load_balancing_scheme}
        :param metadata_filters: metadata_filters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#metadata_filters ComputeGlobalForwardingRule#metadata_filters}
        :param network: This field is not used for external load balancing. For ``INTERNAL`` and ``INTERNAL_SELF_MANAGED`` load balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If this field is not specified, the default network will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#network ComputeGlobalForwardingRule#network}
        :param port_range: When the load balancing scheme is ``EXTERNAL``, ``INTERNAL_SELF_MANAGED`` and ``INTERNAL_MANAGED``, you can specify a ``port_range``. Use with a forwarding rule that points to a target proxy or a target pool. Do not use with a forwarding rule that points to a backend service. This field is used along with the ``target`` field for TargetHttpProxy, TargetHttpsProxy, TargetSslProxy, TargetTcpProxy, TargetVpnGateway, TargetPool, TargetInstance. Applicable only when ``IPProtocol`` is ``TCP``, ``UDP``, or ``SCTP``, only packets addressed to ports in the specified range will be forwarded to ``target``. Forwarding rules with the same ``[IPAddress, IPProtocol]`` pair must have disjoint port ranges. Some types of forwarding target have constraints on the acceptable ports: TargetHttpProxy: 80, 8080 TargetHttpsProxy: 443 TargetTcpProxy: 25, 43, 110, 143, 195, 443, 465, 587, 700, 993, 995, 1688, 1883, 5222 TargetSslProxy: 25, 43, 110, 143, 195, 443, 465, 587, 700, 993, 995, 1688, 1883, 5222 TargetVpnGateway: 500, 4500
        :param project: The project this resource belongs in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#project ComputeGlobalForwardingRule#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#timeouts ComputeGlobalForwardingRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07c6b8df8839697e16cbcd5e3857a8f9633622cc0a8e09c826725c04262fbeb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeGlobalForwardingRuleConfig(
            name=name,
            target=target,
            description=description,
            id=id,
            ip_address=ip_address,
            ip_protocol=ip_protocol,
            ip_version=ip_version,
            labels=labels,
            load_balancing_scheme=load_balancing_scheme,
            metadata_filters=metadata_filters,
            network=network,
            port_range=port_range,
            project=project,
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

    @jsii.member(jsii_name="putMetadataFilters")
    def put_metadata_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3da6aed82913615e21b1e245dbb09143c830e165a8666be04bce3dd900389b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataFilters", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#create ComputeGlobalForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#delete ComputeGlobalForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#update ComputeGlobalForwardingRule#update}.
        '''
        value = ComputeGlobalForwardingRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetIpProtocol")
    def reset_ip_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpProtocol", []))

    @jsii.member(jsii_name="resetIpVersion")
    def reset_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpVersion", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLoadBalancingScheme")
    def reset_load_balancing_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingScheme", []))

    @jsii.member(jsii_name="resetMetadataFilters")
    def reset_metadata_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataFilters", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetPortRange")
    def reset_port_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortRange", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="metadataFilters")
    def metadata_filters(self) -> "ComputeGlobalForwardingRuleMetadataFiltersList":
        return typing.cast("ComputeGlobalForwardingRuleMetadataFiltersList", jsii.get(self, "metadataFilters"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionStatus")
    def psc_connection_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionStatus"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeGlobalForwardingRuleTimeoutsOutputReference":
        return typing.cast("ComputeGlobalForwardingRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="ipVersionInput")
    def ip_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingSchemeInput")
    def load_balancing_scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingSchemeInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataFiltersInput")
    def metadata_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFilters"]]], jsii.get(self, "metadataFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="portRangeInput")
    def port_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["ComputeGlobalForwardingRuleTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ComputeGlobalForwardingRuleTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7396904b9fa6cc3785d9ee1f639d0722d44b1f8c3db2dfbd5840f9c65e50127a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05df454c0bd3584aff5eebae81ab50fd50f7f22d9ed35a9c8d459d98fda5257c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec05748b913f9cf2d81848f50a3713e855c72e331f5cf4951ed65cfba1795ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1974ffc65d8718b70079ff3d85806e2a4b578dcc5311dd44624f48e4c970532f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipVersion"))

    @ip_version.setter
    def ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab37d490f81a1ff4285090e3229e8af901a1a5cabe7bc90b4d66021e2dca607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipVersion", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3599d947c04d4b88ffd0da76af3a4a6fddb2c58f37fc6a1a2d77a467e43f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01956d3d8fc393605654f6ee523bcea5523db6da9584a6189ffc6827c3672b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ec55655ca2e121bd9057038c5dbc03bbd94a93a7535e816aa6dbd8a83c7c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ad46a452b5d9e83d13f9aaa71b63e9244c53365bcc58c6e2b39b2cb72ede08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value)

    @builtins.property
    @jsii.member(jsii_name="portRange")
    def port_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portRange"))

    @port_range.setter
    def port_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83050467b3e420986f10437d51eb071e85a197f5d7a4ca942c38d271b937a52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRange", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65489ee1239755aef95520d70360be444b00f4c1ebe301939b86a6e699db15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314e637db451689b13f3f66ae6b3ba8e446a67d09392d3ffadcd765c83b042c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleConfig",
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
        "target": "target",
        "description": "description",
        "id": "id",
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "ip_version": "ipVersion",
        "labels": "labels",
        "load_balancing_scheme": "loadBalancingScheme",
        "metadata_filters": "metadataFilters",
        "network": "network",
        "port_range": "portRange",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ComputeGlobalForwardingRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[builtins.str] = None,
        port_range: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeGlobalForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression ``[a-z]([-a-z0-9]*[a-z0-9])?`` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must live in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. For ``INTERNAL_SELF_MANAGED`` load balancing, only ``targetHttpProxy`` is valid, not ``targetHttpsProxy``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#target ComputeGlobalForwardingRule#target}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#description ComputeGlobalForwardingRule#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#id ComputeGlobalForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address that this forwarding rule serves. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the target that you specify in the forwarding rule. If you don't specify a reserved IP address, an ephemeral IP address is assigned. Methods for specifying an IP address: * IPv4 dotted decimal, as in ``100.1.2.3`` * Full URL, as in ``https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name`` * Partial URL or by name, as in: * ``projects/project_id/regions/region/addresses/address-name`` * ``regions/region/addresses/address-name`` * ``global/addresses/address-name`` * ``address-name`` The loadBalancingScheme and the forwarding rule's target determine the type of IP address that you can use. For detailed information, refer to `IP address specifications </load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_address ComputeGlobalForwardingRule#ip_address}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are ``TCP``, ``UDP``, ``ESP``, ``AH``, ``SCTP`` or ``ICMP``. For Internal TCP/UDP Load Balancing, the load balancing scheme is ``INTERNAL``, and one of ``TCP`` or ``UDP`` are valid. For Traffic Director, the load balancing scheme is ``INTERNAL_SELF_MANAGED``, and only ``TCP``is valid. For Internal HTTP(S) Load Balancing, the load balancing scheme is ``INTERNAL_MANAGED``, and only ``TCP`` is valid. For HTTP(S), SSL Proxy, and TCP Proxy Load Balancing, the load balancing scheme is ``EXTERNAL`` and only ``TCP`` is valid. For Network TCP/UDP Load Balancing, the load balancing scheme is ``EXTERNAL``, and one of ``TCP`` or ``UDP`` is valid. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_protocol ComputeGlobalForwardingRule#ip_protocol}
        :param ip_version: The IP Version that will be used by this forwarding rule. Valid options are ``IPV4`` or ``IPV6``. This can only be specified for an external global forwarding rule. Possible values: UNSPECIFIED_VERSION, IPV4, IPV6 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_version ComputeGlobalForwardingRule#ip_version}
        :param labels: Labels to apply to this rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#labels ComputeGlobalForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. ``EXTERNAL`` is used for: Classic Cloud VPN gateways Protocol forwarding to VMs from an external IP address The following load balancers: HTTP(S), SSL Proxy, TCP Proxy, and Network TCP/UDP ``INTERNAL`` is used for: Protocol forwarding to VMs from an internal IP address Internal TCP/UDP load balancers ``INTERNAL_MANAGED`` is used for: Internal HTTP(S) load balancers ``INTERNAL_SELF_MANAGED`` is used for: Traffic Director ``EXTERNAL_MANAGED`` is used for: Global external HTTP(S) load balancers For more information about forwarding rules, refer to `Forwarding rule concepts </load-balancing/docs/forwarding-rule-concepts>`_. Possible values: INVALID, INTERNAL, INTERNAL_MANAGED, INTERNAL_SELF_MANAGED, EXTERNAL, EXTERNAL_MANAGED Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#load_balancing_scheme ComputeGlobalForwardingRule#load_balancing_scheme}
        :param metadata_filters: metadata_filters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#metadata_filters ComputeGlobalForwardingRule#metadata_filters}
        :param network: This field is not used for external load balancing. For ``INTERNAL`` and ``INTERNAL_SELF_MANAGED`` load balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If this field is not specified, the default network will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#network ComputeGlobalForwardingRule#network}
        :param port_range: When the load balancing scheme is ``EXTERNAL``, ``INTERNAL_SELF_MANAGED`` and ``INTERNAL_MANAGED``, you can specify a ``port_range``. Use with a forwarding rule that points to a target proxy or a target pool. Do not use with a forwarding rule that points to a backend service. This field is used along with the ``target`` field for TargetHttpProxy, TargetHttpsProxy, TargetSslProxy, TargetTcpProxy, TargetVpnGateway, TargetPool, TargetInstance. Applicable only when ``IPProtocol`` is ``TCP``, ``UDP``, or ``SCTP``, only packets addressed to ports in the specified range will be forwarded to ``target``. Forwarding rules with the same ``[IPAddress, IPProtocol]`` pair must have disjoint port ranges. Some types of forwarding target have constraints on the acceptable ports: TargetHttpProxy: 80, 8080 TargetHttpsProxy: 443 TargetTcpProxy: 25, 43, 110, 143, 195, 443, 465, 587, 700, 993, 995, 1688, 1883, 5222 TargetSslProxy: 25, 43, 110, 143, 195, 443, 465, 587, 700, 993, 995, 1688, 1883, 5222 TargetVpnGateway: 500, 4500
        :param project: The project this resource belongs in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#project ComputeGlobalForwardingRule#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#timeouts ComputeGlobalForwardingRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeGlobalForwardingRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e403e09b2b631185a4e4e82b793529ec650d24fde948a93a328e0c4e06112c46)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument ip_version", value=ip_version, expected_type=type_hints["ip_version"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument metadata_filters", value=metadata_filters, expected_type=type_hints["metadata_filters"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument port_range", value=port_range, expected_type=type_hints["port_range"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "target": target,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if ip_protocol is not None:
            self._values["ip_protocol"] = ip_protocol
        if ip_version is not None:
            self._values["ip_version"] = ip_version
        if labels is not None:
            self._values["labels"] = labels
        if load_balancing_scheme is not None:
            self._values["load_balancing_scheme"] = load_balancing_scheme
        if metadata_filters is not None:
            self._values["metadata_filters"] = metadata_filters
        if network is not None:
            self._values["network"] = network
        if port_range is not None:
            self._values["port_range"] = port_range
        if project is not None:
            self._values["project"] = project
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
    def name(self) -> builtins.str:
        '''Name of the resource;

        provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression ``[a-z]([-a-z0-9]*[a-z0-9])?`` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''The URL of the target resource to receive the matched traffic.

        For regional forwarding rules, this target must live in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. For ``INTERNAL_SELF_MANAGED`` load balancing, only ``targetHttpProxy`` is valid, not ``targetHttpsProxy``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#target ComputeGlobalForwardingRule#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#description ComputeGlobalForwardingRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#id ComputeGlobalForwardingRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''IP address that this forwarding rule serves.

        When a client sends traffic to this IP address, the forwarding rule directs the traffic to the target that you specify in the forwarding rule. If you don't specify a reserved IP address, an ephemeral IP address is assigned. Methods for specifying an IP address: * IPv4 dotted decimal, as in ``100.1.2.3`` * Full URL, as in ``https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name`` * Partial URL or by name, as in: * ``projects/project_id/regions/region/addresses/address-name`` * ``regions/region/addresses/address-name`` * ``global/addresses/address-name`` * ``address-name`` The loadBalancingScheme and the forwarding rule's target determine the type of IP address that you can use. For detailed information, refer to `IP address specifications </load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_address ComputeGlobalForwardingRule#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_protocol(self) -> typing.Optional[builtins.str]:
        '''The IP protocol to which this rule applies.

        For protocol forwarding, valid options are ``TCP``, ``UDP``, ``ESP``, ``AH``, ``SCTP`` or ``ICMP``. For Internal TCP/UDP Load Balancing, the load balancing scheme is ``INTERNAL``, and one of ``TCP`` or ``UDP`` are valid. For Traffic Director, the load balancing scheme is ``INTERNAL_SELF_MANAGED``, and only ``TCP``is valid. For Internal HTTP(S) Load Balancing, the load balancing scheme is ``INTERNAL_MANAGED``, and only ``TCP`` is valid. For HTTP(S), SSL Proxy, and TCP Proxy Load Balancing, the load balancing scheme is ``EXTERNAL`` and only ``TCP`` is valid. For Network TCP/UDP Load Balancing, the load balancing scheme is ``EXTERNAL``, and one of ``TCP`` or ``UDP`` is valid.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_protocol ComputeGlobalForwardingRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_version(self) -> typing.Optional[builtins.str]:
        '''The IP Version that will be used by this forwarding rule.

        Valid options are ``IPV4`` or ``IPV6``. This can only be specified for an external global forwarding rule. Possible values: UNSPECIFIED_VERSION, IPV4, IPV6

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#ip_version ComputeGlobalForwardingRule#ip_version}
        '''
        result = self._values.get("ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#labels ComputeGlobalForwardingRule#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''Specifies the forwarding rule type.

        ``EXTERNAL`` is used for:
        Classic Cloud VPN gateways
        Protocol forwarding to VMs from an external IP address
        The following load balancers: HTTP(S), SSL Proxy, TCP Proxy, and Network TCP/UDP
        ``INTERNAL`` is used for:
        Protocol forwarding to VMs from an internal IP address
        Internal TCP/UDP load balancers
        ``INTERNAL_MANAGED`` is used for:
        Internal HTTP(S) load balancers
        ``INTERNAL_SELF_MANAGED`` is used for:
        Traffic Director
        ``EXTERNAL_MANAGED`` is used for:
        Global external HTTP(S) load balancers

        For more information about forwarding rules, refer to `Forwarding rule concepts </load-balancing/docs/forwarding-rule-concepts>`_. Possible values: INVALID, INTERNAL, INTERNAL_MANAGED, INTERNAL_SELF_MANAGED, EXTERNAL, EXTERNAL_MANAGED

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#load_balancing_scheme ComputeGlobalForwardingRule#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFilters"]]]:
        '''metadata_filters block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#metadata_filters ComputeGlobalForwardingRule#metadata_filters}
        '''
        result = self._values.get("metadata_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFilters"]]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''This field is not used for external load balancing.

        For ``INTERNAL`` and ``INTERNAL_SELF_MANAGED`` load balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If this field is not specified, the default network will be used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#network ComputeGlobalForwardingRule#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_range(self) -> typing.Optional[builtins.str]:
        '''When the load balancing scheme is ``EXTERNAL``, ``INTERNAL_SELF_MANAGED`` and ``INTERNAL_MANAGED``, you can specify a ``port_range``.

        Use with a forwarding rule that points to a target proxy or a target pool. Do not use with a forwarding rule that points to a backend service. This field is used along with the ``target`` field for TargetHttpProxy, TargetHttpsProxy, TargetSslProxy, TargetTcpProxy, TargetVpnGateway, TargetPool, TargetInstance. Applicable only when ``IPProtocol`` is ``TCP``, ``UDP``, or ``SCTP``, only packets addressed to ports in the specified range will be forwarded to ``target``. Forwarding rules with the same ``[IPAddress, IPProtocol]`` pair must have disjoint port ranges. Some types of forwarding target have constraints on the acceptable ports:

        TargetHttpProxy: 80, 8080
        TargetHttpsProxy: 443
        TargetTcpProxy: 25, 43, 110, 143, 195, 443, 465, 587, 700, 993, 995, 1688, 1883, 5222
        TargetSslProxy: 25, 43, 110, 143, 195, 443, 465, 587, 700, 993, 995, 1688, 1883, 5222
        TargetVpnGateway: 500, 4500

        :pattern:

        : d+(?:-d+)?

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#port_range ComputeGlobalForwardingRule#port_range}
        '''
        result = self._values.get("port_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project this resource belongs in.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#project ComputeGlobalForwardingRule#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeGlobalForwardingRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#timeouts ComputeGlobalForwardingRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeGlobalForwardingRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFilters",
    jsii_struct_bases=[],
    name_mapping={
        "filter_labels": "filterLabels",
        "filter_match_criteria": "filterMatchCriteria",
    },
)
class ComputeGlobalForwardingRuleMetadataFilters:
    def __init__(
        self,
        *,
        filter_labels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeGlobalForwardingRuleMetadataFiltersFilterLabels", typing.Dict[builtins.str, typing.Any]]]],
        filter_match_criteria: builtins.str,
    ) -> None:
        '''
        :param filter_labels: filter_labels block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#filter_labels ComputeGlobalForwardingRule#filter_labels}
        :param filter_match_criteria: Specifies how individual ``filterLabel`` matches within the list of ``filterLabel``s contribute towards the overall ``metadataFilter`` match. Supported values are: MATCH_ANY: At least one of the ``filterLabels`` must have a matching label in the provided metadata. MATCH_ALL: All ``filterLabels`` must have matching labels in the provided metadata. Possible values: NOT_SET, MATCH_ALL, MATCH_ANY Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#filter_match_criteria ComputeGlobalForwardingRule#filter_match_criteria}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae3463ee3d611ccea9ea9e5f3668e8a7f945179fe73cc74189ad864e513919a)
            check_type(argname="argument filter_labels", value=filter_labels, expected_type=type_hints["filter_labels"])
            check_type(argname="argument filter_match_criteria", value=filter_match_criteria, expected_type=type_hints["filter_match_criteria"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_labels": filter_labels,
            "filter_match_criteria": filter_match_criteria,
        }

    @builtins.property
    def filter_labels(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFiltersFilterLabels"]]:
        '''filter_labels block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#filter_labels ComputeGlobalForwardingRule#filter_labels}
        '''
        result = self._values.get("filter_labels")
        assert result is not None, "Required property 'filter_labels' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFiltersFilterLabels"]], result)

    @builtins.property
    def filter_match_criteria(self) -> builtins.str:
        '''Specifies how individual ``filterLabel`` matches within the list of ``filterLabel``s contribute towards the overall ``metadataFilter`` match.

        Supported values are:

        MATCH_ANY: At least one of the ``filterLabels`` must have a matching label in the provided metadata.
        MATCH_ALL: All ``filterLabels`` must have matching labels in the provided metadata. Possible values: NOT_SET, MATCH_ALL, MATCH_ANY

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#filter_match_criteria ComputeGlobalForwardingRule#filter_match_criteria}
        '''
        result = self._values.get("filter_match_criteria")
        assert result is not None, "Required property 'filter_match_criteria' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleMetadataFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersFilterLabels",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ComputeGlobalForwardingRuleMetadataFiltersFilterLabels:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of metadata label. The name can have a maximum length of 1024 characters and must be at least 1 character long. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        :param value: The value of the label must match the specified value. value can have a maximum length of 1024 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#value ComputeGlobalForwardingRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecfa75d857dec099070fcfcaf0ffffcdfbcec65330f7c3ff0b67add22b12234)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of metadata label.

        The name can have a maximum length of 1024 characters and must be at least 1 character long.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the label must match the specified value.

        value can have a maximum length of 1024 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#value ComputeGlobalForwardingRule#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleMetadataFiltersFilterLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0256dc72e1cb2a6b0e6ab733e680e5b16b41c5713b4897cb0d91f1fa45b04b92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1b44a2e7731c35da30340240bf46c9f5ab276a7d61678ac268694b279ff2fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9d043f6b5face30e867cb1a6d59297dd530cc19390e9bc2f91aae42db9baba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__336d1873c4387eefefc5161d559d06c36702d1db411a36f16f659fc97a36f7c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b7afe22e7517ff87f51dafc1a5f123455b382eafb90b7b0ac562e2192f9df61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579f5898101e8ed379295e473748f9f129d33883350f7e1feaa5e9eac901d32d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1f3ba113f612ab0f3ed58e911371462efab09b550f1a30a96c0168a16e439c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a785af3ce6e77a7f8d15cc30aefd33984fb774fe5b90b38aaf9434c3b2dcae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9591135e33691bd2c47e35b1888773b89ed2e833eee9c00fe69c6e98f0e01474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa55770f37104c3ed4562ceef0a36d22ac23abe554abe65964d362773e7f2e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeGlobalForwardingRuleMetadataFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d23a3fb369a8e25b0a267e7f885c01fdad124ba08601ebc201371f133a9aa00f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeGlobalForwardingRuleMetadataFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b286c98fb415450bb2cb6253ae45a243bee1bc9429e61f89c367e88e33de05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeGlobalForwardingRuleMetadataFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b71511edf1db94bbc319433facfe9c20d8dd990cf4b9597f546e76a460fb8bb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f536524257da377d6479fbd6aad8133124a20b416d28e0270aa6b328c0d3fb2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb28c0b9801ca46ff358ce3a1eb6e3a09300870335f0df7bc2a8a7a70cd17829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a511060dab1ad6ef10dd579724eb9d21546d7791c77fb03886c16bcdf3f359e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeGlobalForwardingRuleMetadataFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46e8764eb6ea807e5541e7728c459aa3720391fd640ce74094a374ca13a4a683)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilterLabels")
    def put_filter_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b03d252ce96b4c565039680e5c0ffef871f6454619a126085e1dcf714d20fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilterLabels", [value]))

    @builtins.property
    @jsii.member(jsii_name="filterLabels")
    def filter_labels(
        self,
    ) -> ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList:
        return typing.cast(ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList, jsii.get(self, "filterLabels"))

    @builtins.property
    @jsii.member(jsii_name="filterLabelsInput")
    def filter_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]], jsii.get(self, "filterLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="filterMatchCriteriaInput")
    def filter_match_criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterMatchCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="filterMatchCriteria")
    def filter_match_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterMatchCriteria"))

    @filter_match_criteria.setter
    def filter_match_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fff1bcaa1c75228ae6362bd55f1b8603e62fddcef4cc2fad4436788fc9e400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterMatchCriteria", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53002c926cb97a225d3d55fc9c62cf0fce64e51dab35107f78e6350a16f64de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeGlobalForwardingRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#create ComputeGlobalForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#delete ComputeGlobalForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#update ComputeGlobalForwardingRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76058cca11fe4fd284279603d636b8cf18e27eb31e82b906e36169496aed93f8)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#create ComputeGlobalForwardingRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#delete ComputeGlobalForwardingRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_global_forwarding_rule#update ComputeGlobalForwardingRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeGlobalForwardingRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__961e4612af4e06848e69b441d4f4435a9369e0ffd8fd98e4d4a02ad1c2d1cc9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97f805bdfb2ae64c2f0711977e2ce52703a1cce4d4862ae6c2dd1e8244bdde01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e06f1828edc598cf9c652630ae406ee0f42c522a8d73ccf438e8e229c8deb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8717a5a27635f9f7acc5c86034ca8130d1fa359085c4b55fb2b9a745c2a82968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ComputeGlobalForwardingRuleTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeGlobalForwardingRuleTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeGlobalForwardingRuleTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de59a92ee11b84b5480f9fe27da6b40229acdb8b1aec74b49d32ad63c7d266fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ComputeGlobalForwardingRule",
    "ComputeGlobalForwardingRuleConfig",
    "ComputeGlobalForwardingRuleMetadataFilters",
    "ComputeGlobalForwardingRuleMetadataFiltersFilterLabels",
    "ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList",
    "ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference",
    "ComputeGlobalForwardingRuleMetadataFiltersList",
    "ComputeGlobalForwardingRuleMetadataFiltersOutputReference",
    "ComputeGlobalForwardingRuleTimeouts",
    "ComputeGlobalForwardingRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a07c6b8df8839697e16cbcd5e3857a8f9633622cc0a8e09c826725c04262fbeb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[builtins.str] = None,
    port_range: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeGlobalForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ec3da6aed82913615e21b1e245dbb09143c830e165a8666be04bce3dd900389b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7396904b9fa6cc3785d9ee1f639d0722d44b1f8c3db2dfbd5840f9c65e50127a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05df454c0bd3584aff5eebae81ab50fd50f7f22d9ed35a9c8d459d98fda5257c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec05748b913f9cf2d81848f50a3713e855c72e331f5cf4951ed65cfba1795ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1974ffc65d8718b70079ff3d85806e2a4b578dcc5311dd44624f48e4c970532f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab37d490f81a1ff4285090e3229e8af901a1a5cabe7bc90b4d66021e2dca607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3599d947c04d4b88ffd0da76af3a4a6fddb2c58f37fc6a1a2d77a467e43f64(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01956d3d8fc393605654f6ee523bcea5523db6da9584a6189ffc6827c3672b78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ec55655ca2e121bd9057038c5dbc03bbd94a93a7535e816aa6dbd8a83c7c7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ad46a452b5d9e83d13f9aaa71b63e9244c53365bcc58c6e2b39b2cb72ede08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83050467b3e420986f10437d51eb071e85a197f5d7a4ca942c38d271b937a52a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65489ee1239755aef95520d70360be444b00f4c1ebe301939b86a6e699db15f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314e637db451689b13f3f66ae6b3ba8e446a67d09392d3ffadcd765c83b042c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e403e09b2b631185a4e4e82b793529ec650d24fde948a93a328e0c4e06112c46(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[builtins.str] = None,
    port_range: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeGlobalForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae3463ee3d611ccea9ea9e5f3668e8a7f945179fe73cc74189ad864e513919a(
    *,
    filter_labels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
    filter_match_criteria: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecfa75d857dec099070fcfcaf0ffffcdfbcec65330f7c3ff0b67add22b12234(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0256dc72e1cb2a6b0e6ab733e680e5b16b41c5713b4897cb0d91f1fa45b04b92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1b44a2e7731c35da30340240bf46c9f5ab276a7d61678ac268694b279ff2fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9d043f6b5face30e867cb1a6d59297dd530cc19390e9bc2f91aae42db9baba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336d1873c4387eefefc5161d559d06c36702d1db411a36f16f659fc97a36f7c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7afe22e7517ff87f51dafc1a5f123455b382eafb90b7b0ac562e2192f9df61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579f5898101e8ed379295e473748f9f129d33883350f7e1feaa5e9eac901d32d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1f3ba113f612ab0f3ed58e911371462efab09b550f1a30a96c0168a16e439c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a785af3ce6e77a7f8d15cc30aefd33984fb774fe5b90b38aaf9434c3b2dcae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9591135e33691bd2c47e35b1888773b89ed2e833eee9c00fe69c6e98f0e01474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa55770f37104c3ed4562ceef0a36d22ac23abe554abe65964d362773e7f2e06(
    value: typing.Optional[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23a3fb369a8e25b0a267e7f885c01fdad124ba08601ebc201371f133a9aa00f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b286c98fb415450bb2cb6253ae45a243bee1bc9429e61f89c367e88e33de05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71511edf1db94bbc319433facfe9c20d8dd990cf4b9597f546e76a460fb8bb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f536524257da377d6479fbd6aad8133124a20b416d28e0270aa6b328c0d3fb2d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb28c0b9801ca46ff358ce3a1eb6e3a09300870335f0df7bc2a8a7a70cd17829(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a511060dab1ad6ef10dd579724eb9d21546d7791c77fb03886c16bcdf3f359e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e8764eb6ea807e5541e7728c459aa3720391fd640ce74094a374ca13a4a683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b03d252ce96b4c565039680e5c0ffef871f6454619a126085e1dcf714d20fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fff1bcaa1c75228ae6362bd55f1b8603e62fddcef4cc2fad4436788fc9e400(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53002c926cb97a225d3d55fc9c62cf0fce64e51dab35107f78e6350a16f64de(
    value: typing.Optional[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76058cca11fe4fd284279603d636b8cf18e27eb31e82b906e36169496aed93f8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961e4612af4e06848e69b441d4f4435a9369e0ffd8fd98e4d4a02ad1c2d1cc9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f805bdfb2ae64c2f0711977e2ce52703a1cce4d4862ae6c2dd1e8244bdde01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e06f1828edc598cf9c652630ae406ee0f42c522a8d73ccf438e8e229c8deb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8717a5a27635f9f7acc5c86034ca8130d1fa359085c4b55fb2b9a745c2a82968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de59a92ee11b84b5480f9fe27da6b40229acdb8b1aec74b49d32ad63c7d266fc(
    value: typing.Optional[typing.Union[ComputeGlobalForwardingRuleTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
