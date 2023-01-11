'''
# `cloudflare_load_balancer`

Refer to the Terraform Registory for docs: [`cloudflare_load_balancer`](https://www.terraform.io/docs/providers/cloudflare/r/load_balancer).
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


class LoadBalancer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancer",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer cloudflare_load_balancer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_pool_ids: typing.Sequence[builtins.str],
        fallback_pool_id: builtins.str,
        name: builtins.str,
        zone_id: builtins.str,
        adaptive_routing: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerAdaptiveRouting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        country_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerCountryPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        location_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerLocationStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pop_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPopPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        proxied: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        random_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRandomSteering", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRegionPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        session_affinity_ttl: typing.Optional[jsii.Number] = None,
        steering_policy: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer cloudflare_load_balancer} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_pool_ids: A list of pool IDs ordered by their failover priority. Used whenever ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_ are not defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_pool_ids LoadBalancer#default_pool_ids}
        :param fallback_pool_id: The pool ID to use when all other pools are detected as unhealthy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#fallback_pool_id LoadBalancer#fallback_pool_id}
        :param name: The DNS hostname to associate with your load balancer. If this hostname already exists as a DNS record in Cloudflare's DNS, the load balancer will take precedence and the DNS record will not be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#name LoadBalancer#name}
        :param zone_id: The zone ID to add the load balancer to. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#zone_id LoadBalancer#zone_id}
        :param adaptive_routing: adaptive_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#adaptive_routing LoadBalancer#adaptive_routing}
        :param country_pools: country_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country_pools LoadBalancer#country_pools}
        :param description: Free text description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#description LoadBalancer#description}
        :param enabled: Enable or disable the load balancer. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#enabled LoadBalancer#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#id LoadBalancer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location_strategy: location_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#location_strategy LoadBalancer#location_strategy}
        :param pop_pools: pop_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop_pools LoadBalancer#pop_pools}
        :param proxied: Whether the hostname gets Cloudflare's origin protection. Defaults to ``false``. Conflicts with ``ttl``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#proxied LoadBalancer#proxied}
        :param random_steering: random_steering block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#random_steering LoadBalancer#random_steering}
        :param region_pools: region_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region_pools LoadBalancer#region_pools}
        :param rules: rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#rules LoadBalancer#rules}
        :param session_affinity: Specifies the type of session affinity the load balancer should use unless specified as ``none`` or ``""`` (default). With value ``cookie``, on the first request to a proxied load balancer, a cookie is generated, encoding information of which origin the request will be forwarded to. Subsequent requests, by the same client to the same load balancer, will be sent to the origin server the cookie encodes, for the duration of the cookie and as long as the origin server remains healthy. If the cookie has expired or the origin server is unhealthy then a new origin server is calculated and used. Value ``ip_cookie`` behaves the same as ``cookie`` except the initial origin selection is stable and based on the client's IP address. Available values: ``""``, ``none``, ``cookie``, ``ip_cookie``. Defaults to ``none``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity LoadBalancer#session_affinity}
        :param session_affinity_attributes: See ```session_affinity_attributes`` <#nested-schema-for-session_affinity_attributes>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_attributes LoadBalancer#session_affinity_attributes}
        :param session_affinity_ttl: Time, in seconds, until this load balancer's session affinity cookie expires after being created. This parameter is ignored unless a supported session affinity policy is set. The current default of ``82800`` (23 hours) will be used unless ```session_affinity_ttl`` <#session_affinity_ttl>`_ is explicitly set. Once the expiry time has been reached, subsequent requests may get sent to a different origin server. Valid values are between ``1800`` and ``604800``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_ttl LoadBalancer#session_affinity_ttl}
        :param steering_policy: The method the load balancer uses to determine the route to your origin. Value ``off`` uses ```default_pool_ids`` <#default_pool_ids>`_. Value ``geo`` uses ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_. For non-proxied requests, the ```country`` <#country>`_ for ```country_pools`` <#country_pools>`_ is determined by ```location_strategy`` <#location_strategy>`_. Value ``random`` selects a pool randomly. Value ``dynamic_latency`` uses round trip time to select the closest pool in ```default_pool_ids`` <#default_pool_ids>`_ (requires pool health checks). Value ``proximity`` uses the pools' latitude and longitude to select the closest pool using the Cloudflare PoP location for proxied requests or the location determined by ```location_strategy`` <#location_strategy>`_ for non-proxied requests. Value ``""`` maps to ``geo`` if you use ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_ otherwise ``off``. Available values: ``off``, ``geo``, ``dynamic_latency``, ``random``, ``proximity``, ``""`` Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#steering_policy LoadBalancer#steering_policy}
        :param ttl: Time to live (TTL) of the DNS entry for the IP address returned by this load balancer. This cannot be set for proxied load balancers. Defaults to ``30``. Conflicts with ``proxied``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#ttl LoadBalancer#ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0015049507828df93e92dfe6c1bca8e51a3ffecfec278ed1f472e11b1c5ed18f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LoadBalancerConfig(
            default_pool_ids=default_pool_ids,
            fallback_pool_id=fallback_pool_id,
            name=name,
            zone_id=zone_id,
            adaptive_routing=adaptive_routing,
            country_pools=country_pools,
            description=description,
            enabled=enabled,
            id=id,
            location_strategy=location_strategy,
            pop_pools=pop_pools,
            proxied=proxied,
            random_steering=random_steering,
            region_pools=region_pools,
            rules=rules,
            session_affinity=session_affinity,
            session_affinity_attributes=session_affinity_attributes,
            session_affinity_ttl=session_affinity_ttl,
            steering_policy=steering_policy,
            ttl=ttl,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAdaptiveRouting")
    def put_adaptive_routing(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerAdaptiveRouting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd71b604d790772dd1e1e7eea42b70abcce9e3b559a9a9b30a69670c92ccbc65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdaptiveRouting", [value]))

    @jsii.member(jsii_name="putCountryPools")
    def put_country_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerCountryPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50edfbde3fcf807556ccbf4a3c2735ad986bc9671861528170233fc398dacb9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCountryPools", [value]))

    @jsii.member(jsii_name="putLocationStrategy")
    def put_location_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerLocationStrategy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e05171f7beaedecec9431cd699717abfa6649fd62970384440f38de6f09e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocationStrategy", [value]))

    @jsii.member(jsii_name="putPopPools")
    def put_pop_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPopPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f2d23803906f9e0aa584834529e26d8492a405660336bfb106e903130394a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPopPools", [value]))

    @jsii.member(jsii_name="putRandomSteering")
    def put_random_steering(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRandomSteering", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec78a491daf142014840778ab5eaf966681a5818db093b6dfa84b5b9fd485a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRandomSteering", [value]))

    @jsii.member(jsii_name="putRegionPools")
    def put_region_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRegionPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9adcb40f3b9090ef6dd1e7ceab37de12506e140f848103406a4e1e1b69039ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegionPools", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713bf22a49b1560498a800316f840069503b2323554a05dc728d48b4c9dca764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetAdaptiveRouting")
    def reset_adaptive_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdaptiveRouting", []))

    @jsii.member(jsii_name="resetCountryPools")
    def reset_country_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryPools", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocationStrategy")
    def reset_location_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationStrategy", []))

    @jsii.member(jsii_name="resetPopPools")
    def reset_pop_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPopPools", []))

    @jsii.member(jsii_name="resetProxied")
    def reset_proxied(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxied", []))

    @jsii.member(jsii_name="resetRandomSteering")
    def reset_random_steering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRandomSteering", []))

    @jsii.member(jsii_name="resetRegionPools")
    def reset_region_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionPools", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @jsii.member(jsii_name="resetSessionAffinity")
    def reset_session_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinity", []))

    @jsii.member(jsii_name="resetSessionAffinityAttributes")
    def reset_session_affinity_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinityAttributes", []))

    @jsii.member(jsii_name="resetSessionAffinityTtl")
    def reset_session_affinity_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinityTtl", []))

    @jsii.member(jsii_name="resetSteeringPolicy")
    def reset_steering_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSteeringPolicy", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="adaptiveRouting")
    def adaptive_routing(self) -> "LoadBalancerAdaptiveRoutingList":
        return typing.cast("LoadBalancerAdaptiveRoutingList", jsii.get(self, "adaptiveRouting"))

    @builtins.property
    @jsii.member(jsii_name="countryPools")
    def country_pools(self) -> "LoadBalancerCountryPoolsList":
        return typing.cast("LoadBalancerCountryPoolsList", jsii.get(self, "countryPools"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="locationStrategy")
    def location_strategy(self) -> "LoadBalancerLocationStrategyList":
        return typing.cast("LoadBalancerLocationStrategyList", jsii.get(self, "locationStrategy"))

    @builtins.property
    @jsii.member(jsii_name="modifiedOn")
    def modified_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="popPools")
    def pop_pools(self) -> "LoadBalancerPopPoolsList":
        return typing.cast("LoadBalancerPopPoolsList", jsii.get(self, "popPools"))

    @builtins.property
    @jsii.member(jsii_name="randomSteering")
    def random_steering(self) -> "LoadBalancerRandomSteeringList":
        return typing.cast("LoadBalancerRandomSteeringList", jsii.get(self, "randomSteering"))

    @builtins.property
    @jsii.member(jsii_name="regionPools")
    def region_pools(self) -> "LoadBalancerRegionPoolsList":
        return typing.cast("LoadBalancerRegionPoolsList", jsii.get(self, "regionPools"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "LoadBalancerRulesList":
        return typing.cast("LoadBalancerRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="adaptiveRoutingInput")
    def adaptive_routing_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerAdaptiveRouting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerAdaptiveRouting"]]], jsii.get(self, "adaptiveRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="countryPoolsInput")
    def country_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerCountryPools"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerCountryPools"]]], jsii.get(self, "countryPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPoolIdsInput")
    def default_pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "defaultPoolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackPoolIdInput")
    def fallback_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fallbackPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationStrategyInput")
    def location_strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerLocationStrategy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerLocationStrategy"]]], jsii.get(self, "locationStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="popPoolsInput")
    def pop_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPopPools"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPopPools"]]], jsii.get(self, "popPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="proxiedInput")
    def proxied_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "proxiedInput"))

    @builtins.property
    @jsii.member(jsii_name="randomSteeringInput")
    def random_steering_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRandomSteering"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRandomSteering"]]], jsii.get(self, "randomSteeringInput"))

    @builtins.property
    @jsii.member(jsii_name="regionPoolsInput")
    def region_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRegionPools"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRegionPools"]]], jsii.get(self, "regionPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityAttributesInput")
    def session_affinity_attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sessionAffinityAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityTtlInput")
    def session_affinity_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionAffinityTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="steeringPolicyInput")
    def steering_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "steeringPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPoolIds")
    def default_pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultPoolIds"))

    @default_pool_ids.setter
    def default_pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6089aef46269616117102dcd766828c839cd34a6ddc1a19b167be40df8a74eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPoolIds", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749c6dd92b9de55f6f692a104109a7a8c0140668d57a671f2f4096578fa936a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__83c6dec4fe321e227c8d9680880282305431f4dba6c380b6d1257f0b33508764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="fallbackPoolId")
    def fallback_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fallbackPoolId"))

    @fallback_pool_id.setter
    def fallback_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c848e190f535b767ecfa8d3c11f67ea8f02df867f678e83a7accbe2fcc7c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fallbackPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee843cb964fbfddfe418aaaae462d730e400aab7fa1dc269ff018bb76f0398dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549a6fc7dd52b05e493a75e851006eb3ff4b1b5be4e31f42a3e0fba8a3e7992c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="proxied")
    def proxied(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "proxied"))

    @proxied.setter
    def proxied(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e098d3c0597e3524b55c3627f9a3bb7992a85e831d4f688b06dfff6966b3988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxied", value)

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0750582d833b47b92d0f19d520eb3c3efdee362ea8a4097af61978e00dce967a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value)

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityAttributes")
    def session_affinity_attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sessionAffinityAttributes"))

    @session_affinity_attributes.setter
    def session_affinity_attributes(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd986c02bbc00cd38b69d6b9650c1f90ba2f88202d3989cddfc70f5f1707c0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinityAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityTtl")
    def session_affinity_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionAffinityTtl"))

    @session_affinity_ttl.setter
    def session_affinity_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0cd47fb3f2073bbd91e71dcb6d52e072ba67430ce8b3bd46319e7ae25f9afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinityTtl", value)

    @builtins.property
    @jsii.member(jsii_name="steeringPolicy")
    def steering_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "steeringPolicy"))

    @steering_policy.setter
    def steering_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38cc45e4ba523e71f68dc6122fbd27e2295e3f03fc8776d0f26210fe4925bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "steeringPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fcc62043aca63d073f33eb1730d5f1b0708a90f7fa61ae55fbbe0cebee22ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21bb86cc37c1ec4ce7603426eab2a13a53a3024685a2262c80dcf7351190a31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerAdaptiveRouting",
    jsii_struct_bases=[],
    name_mapping={"failover_across_pools": "failoverAcrossPools"},
)
class LoadBalancerAdaptiveRouting:
    def __init__(
        self,
        *,
        failover_across_pools: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param failover_across_pools: Extends zero-downtime failover of requests to healthy origins from alternate pools, when no healthy alternate exists in the same pool, according to the failover order defined by traffic and origin steering. When set ``false``, zero-downtime failover will only occur between origins within the same pool. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#failover_across_pools LoadBalancer#failover_across_pools}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303c8d660d7ff911b7607b1ed365324cf95aef52ab574f4228534f17fbfe1953)
            check_type(argname="argument failover_across_pools", value=failover_across_pools, expected_type=type_hints["failover_across_pools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failover_across_pools is not None:
            self._values["failover_across_pools"] = failover_across_pools

    @builtins.property
    def failover_across_pools(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Extends zero-downtime failover of requests to healthy origins from alternate pools, when no healthy alternate exists in the same pool, according to the failover order defined by traffic and origin steering.

        When set ``false``, zero-downtime failover will only occur between origins within the same pool. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#failover_across_pools LoadBalancer#failover_across_pools}
        '''
        result = self._values.get("failover_across_pools")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerAdaptiveRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerAdaptiveRoutingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerAdaptiveRoutingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a90b6e6790528c206468d640490db3abef5a8c6eebaf718a4dd4418812b68081)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerAdaptiveRoutingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1559fb373ea400511817842976f6481ca4b702ec9d77caf629d01b47a72a6b80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerAdaptiveRoutingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72195fa870c62adbc2009d6ce6bcee0c275b9d355f65d6f5e8d9817c53c256db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83acfa63a7027123b02704d5e9a579ece4765d5ebc3c69f7ca90b31ac6ee89cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c506b6e06e7598e4219c30ddbe89a9325a76d05e43f16817b52d09bd0c01095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerAdaptiveRouting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerAdaptiveRouting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerAdaptiveRouting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3b4a1d4e77121ca9e6e6252584e0995b5d384fbc3f3c004f6c162fdc221751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerAdaptiveRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerAdaptiveRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d41d79f69f4c4baa892cc9881ebe8a3b44e49a9e164ded9e679d66e3b05302c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFailoverAcrossPools")
    def reset_failover_across_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverAcrossPools", []))

    @builtins.property
    @jsii.member(jsii_name="failoverAcrossPoolsInput")
    def failover_across_pools_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failoverAcrossPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverAcrossPools")
    def failover_across_pools(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failoverAcrossPools"))

    @failover_across_pools.setter
    def failover_across_pools(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483f29751055bdcab9b5325a954524c06820b6aca2f5bdcef6272c6c5e8f633d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverAcrossPools", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerAdaptiveRouting, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerAdaptiveRouting, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerAdaptiveRouting, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4657374ad9caf633eb09b1d65ba4e5b4f17d06e0b28714a28b13cdc210bd62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_pool_ids": "defaultPoolIds",
        "fallback_pool_id": "fallbackPoolId",
        "name": "name",
        "zone_id": "zoneId",
        "adaptive_routing": "adaptiveRouting",
        "country_pools": "countryPools",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "location_strategy": "locationStrategy",
        "pop_pools": "popPools",
        "proxied": "proxied",
        "random_steering": "randomSteering",
        "region_pools": "regionPools",
        "rules": "rules",
        "session_affinity": "sessionAffinity",
        "session_affinity_attributes": "sessionAffinityAttributes",
        "session_affinity_ttl": "sessionAffinityTtl",
        "steering_policy": "steeringPolicy",
        "ttl": "ttl",
    },
)
class LoadBalancerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_pool_ids: typing.Sequence[builtins.str],
        fallback_pool_id: builtins.str,
        name: builtins.str,
        zone_id: builtins.str,
        adaptive_routing: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerAdaptiveRouting, typing.Dict[builtins.str, typing.Any]]]]] = None,
        country_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerCountryPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        location_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerLocationStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pop_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPopPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        proxied: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        random_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRandomSteering", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRegionPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        session_affinity_ttl: typing.Optional[jsii.Number] = None,
        steering_policy: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_pool_ids: A list of pool IDs ordered by their failover priority. Used whenever ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_ are not defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_pool_ids LoadBalancer#default_pool_ids}
        :param fallback_pool_id: The pool ID to use when all other pools are detected as unhealthy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#fallback_pool_id LoadBalancer#fallback_pool_id}
        :param name: The DNS hostname to associate with your load balancer. If this hostname already exists as a DNS record in Cloudflare's DNS, the load balancer will take precedence and the DNS record will not be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#name LoadBalancer#name}
        :param zone_id: The zone ID to add the load balancer to. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#zone_id LoadBalancer#zone_id}
        :param adaptive_routing: adaptive_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#adaptive_routing LoadBalancer#adaptive_routing}
        :param country_pools: country_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country_pools LoadBalancer#country_pools}
        :param description: Free text description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#description LoadBalancer#description}
        :param enabled: Enable or disable the load balancer. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#enabled LoadBalancer#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#id LoadBalancer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location_strategy: location_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#location_strategy LoadBalancer#location_strategy}
        :param pop_pools: pop_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop_pools LoadBalancer#pop_pools}
        :param proxied: Whether the hostname gets Cloudflare's origin protection. Defaults to ``false``. Conflicts with ``ttl``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#proxied LoadBalancer#proxied}
        :param random_steering: random_steering block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#random_steering LoadBalancer#random_steering}
        :param region_pools: region_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region_pools LoadBalancer#region_pools}
        :param rules: rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#rules LoadBalancer#rules}
        :param session_affinity: Specifies the type of session affinity the load balancer should use unless specified as ``none`` or ``""`` (default). With value ``cookie``, on the first request to a proxied load balancer, a cookie is generated, encoding information of which origin the request will be forwarded to. Subsequent requests, by the same client to the same load balancer, will be sent to the origin server the cookie encodes, for the duration of the cookie and as long as the origin server remains healthy. If the cookie has expired or the origin server is unhealthy then a new origin server is calculated and used. Value ``ip_cookie`` behaves the same as ``cookie`` except the initial origin selection is stable and based on the client's IP address. Available values: ``""``, ``none``, ``cookie``, ``ip_cookie``. Defaults to ``none``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity LoadBalancer#session_affinity}
        :param session_affinity_attributes: See ```session_affinity_attributes`` <#nested-schema-for-session_affinity_attributes>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_attributes LoadBalancer#session_affinity_attributes}
        :param session_affinity_ttl: Time, in seconds, until this load balancer's session affinity cookie expires after being created. This parameter is ignored unless a supported session affinity policy is set. The current default of ``82800`` (23 hours) will be used unless ```session_affinity_ttl`` <#session_affinity_ttl>`_ is explicitly set. Once the expiry time has been reached, subsequent requests may get sent to a different origin server. Valid values are between ``1800`` and ``604800``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_ttl LoadBalancer#session_affinity_ttl}
        :param steering_policy: The method the load balancer uses to determine the route to your origin. Value ``off`` uses ```default_pool_ids`` <#default_pool_ids>`_. Value ``geo`` uses ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_. For non-proxied requests, the ```country`` <#country>`_ for ```country_pools`` <#country_pools>`_ is determined by ```location_strategy`` <#location_strategy>`_. Value ``random`` selects a pool randomly. Value ``dynamic_latency`` uses round trip time to select the closest pool in ```default_pool_ids`` <#default_pool_ids>`_ (requires pool health checks). Value ``proximity`` uses the pools' latitude and longitude to select the closest pool using the Cloudflare PoP location for proxied requests or the location determined by ```location_strategy`` <#location_strategy>`_ for non-proxied requests. Value ``""`` maps to ``geo`` if you use ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_ otherwise ``off``. Available values: ``off``, ``geo``, ``dynamic_latency``, ``random``, ``proximity``, ``""`` Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#steering_policy LoadBalancer#steering_policy}
        :param ttl: Time to live (TTL) of the DNS entry for the IP address returned by this load balancer. This cannot be set for proxied load balancers. Defaults to ``30``. Conflicts with ``proxied``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#ttl LoadBalancer#ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179a274ba88b1187743571bdcd7d729435f5abbf8faf21f1b93231a9af798a1f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_pool_ids", value=default_pool_ids, expected_type=type_hints["default_pool_ids"])
            check_type(argname="argument fallback_pool_id", value=fallback_pool_id, expected_type=type_hints["fallback_pool_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument adaptive_routing", value=adaptive_routing, expected_type=type_hints["adaptive_routing"])
            check_type(argname="argument country_pools", value=country_pools, expected_type=type_hints["country_pools"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location_strategy", value=location_strategy, expected_type=type_hints["location_strategy"])
            check_type(argname="argument pop_pools", value=pop_pools, expected_type=type_hints["pop_pools"])
            check_type(argname="argument proxied", value=proxied, expected_type=type_hints["proxied"])
            check_type(argname="argument random_steering", value=random_steering, expected_type=type_hints["random_steering"])
            check_type(argname="argument region_pools", value=region_pools, expected_type=type_hints["region_pools"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument session_affinity_attributes", value=session_affinity_attributes, expected_type=type_hints["session_affinity_attributes"])
            check_type(argname="argument session_affinity_ttl", value=session_affinity_ttl, expected_type=type_hints["session_affinity_ttl"])
            check_type(argname="argument steering_policy", value=steering_policy, expected_type=type_hints["steering_policy"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_pool_ids": default_pool_ids,
            "fallback_pool_id": fallback_pool_id,
            "name": name,
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
        if adaptive_routing is not None:
            self._values["adaptive_routing"] = adaptive_routing
        if country_pools is not None:
            self._values["country_pools"] = country_pools
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if location_strategy is not None:
            self._values["location_strategy"] = location_strategy
        if pop_pools is not None:
            self._values["pop_pools"] = pop_pools
        if proxied is not None:
            self._values["proxied"] = proxied
        if random_steering is not None:
            self._values["random_steering"] = random_steering
        if region_pools is not None:
            self._values["region_pools"] = region_pools
        if rules is not None:
            self._values["rules"] = rules
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if session_affinity_attributes is not None:
            self._values["session_affinity_attributes"] = session_affinity_attributes
        if session_affinity_ttl is not None:
            self._values["session_affinity_ttl"] = session_affinity_ttl
        if steering_policy is not None:
            self._values["steering_policy"] = steering_policy
        if ttl is not None:
            self._values["ttl"] = ttl

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
    def default_pool_ids(self) -> typing.List[builtins.str]:
        '''A list of pool IDs ordered by their failover priority. Used whenever ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_ are not defined.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_pool_ids LoadBalancer#default_pool_ids}
        '''
        result = self._values.get("default_pool_ids")
        assert result is not None, "Required property 'default_pool_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fallback_pool_id(self) -> builtins.str:
        '''The pool ID to use when all other pools are detected as unhealthy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#fallback_pool_id LoadBalancer#fallback_pool_id}
        '''
        result = self._values.get("fallback_pool_id")
        assert result is not None, "Required property 'fallback_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The DNS hostname to associate with your load balancer.

        If this hostname already exists as a DNS record in Cloudflare's DNS, the load balancer will take precedence and the DNS record will not be used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#name LoadBalancer#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''The zone ID to add the load balancer to. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#zone_id LoadBalancer#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def adaptive_routing(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerAdaptiveRouting]]]:
        '''adaptive_routing block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#adaptive_routing LoadBalancer#adaptive_routing}
        '''
        result = self._values.get("adaptive_routing")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerAdaptiveRouting]]], result)

    @builtins.property
    def country_pools(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerCountryPools"]]]:
        '''country_pools block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country_pools LoadBalancer#country_pools}
        '''
        result = self._values.get("country_pools")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerCountryPools"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Free text description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#description LoadBalancer#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable the load balancer. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#enabled LoadBalancer#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#id LoadBalancer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerLocationStrategy"]]]:
        '''location_strategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#location_strategy LoadBalancer#location_strategy}
        '''
        result = self._values.get("location_strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerLocationStrategy"]]], result)

    @builtins.property
    def pop_pools(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPopPools"]]]:
        '''pop_pools block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop_pools LoadBalancer#pop_pools}
        '''
        result = self._values.get("pop_pools")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPopPools"]]], result)

    @builtins.property
    def proxied(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the hostname gets Cloudflare's origin protection. Defaults to ``false``. Conflicts with ``ttl``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#proxied LoadBalancer#proxied}
        '''
        result = self._values.get("proxied")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def random_steering(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRandomSteering"]]]:
        '''random_steering block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#random_steering LoadBalancer#random_steering}
        '''
        result = self._values.get("random_steering")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRandomSteering"]]], result)

    @builtins.property
    def region_pools(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRegionPools"]]]:
        '''region_pools block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region_pools LoadBalancer#region_pools}
        '''
        result = self._values.get("region_pools")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRegionPools"]]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#rules LoadBalancer#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRules"]]], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of session affinity the load balancer should use unless specified as ``none`` or ``""`` (default).

        With value ``cookie``, on the first request to a proxied load balancer, a cookie is generated, encoding information of which origin the request will be forwarded to. Subsequent requests, by the same client to the same load balancer, will be sent to the origin server the cookie encodes, for the duration of the cookie and as long as the origin server remains healthy. If the cookie has expired or the origin server is unhealthy then a new origin server is calculated and used. Value ``ip_cookie`` behaves the same as ``cookie`` except the initial origin selection is stable and based on the client's IP address. Available values: ``""``, ``none``, ``cookie``, ``ip_cookie``. Defaults to ``none``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity LoadBalancer#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''See ```session_affinity_attributes`` <#nested-schema-for-session_affinity_attributes>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_attributes LoadBalancer#session_affinity_attributes}
        '''
        result = self._values.get("session_affinity_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def session_affinity_ttl(self) -> typing.Optional[jsii.Number]:
        '''Time, in seconds, until this load balancer's session affinity cookie expires after being created.

        This parameter is ignored unless a supported session affinity policy is set. The current default of ``82800`` (23 hours) will be used unless ```session_affinity_ttl`` <#session_affinity_ttl>`_ is explicitly set. Once the expiry time has been reached, subsequent requests may get sent to a different origin server. Valid values are between ``1800`` and ``604800``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_ttl LoadBalancer#session_affinity_ttl}
        '''
        result = self._values.get("session_affinity_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def steering_policy(self) -> typing.Optional[builtins.str]:
        '''The method the load balancer uses to determine the route to your origin.

        Value ``off`` uses ```default_pool_ids`` <#default_pool_ids>`_. Value ``geo`` uses ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_. For non-proxied requests, the ```country`` <#country>`_ for ```country_pools`` <#country_pools>`_ is determined by ```location_strategy`` <#location_strategy>`_. Value ``random`` selects a pool randomly. Value ``dynamic_latency`` uses round trip time to select the closest pool in ```default_pool_ids`` <#default_pool_ids>`_ (requires pool health checks). Value ``proximity`` uses the pools' latitude and longitude to select the closest pool using the Cloudflare PoP location for proxied requests or the location determined by ```location_strategy`` <#location_strategy>`_ for non-proxied requests. Value ``""`` maps to ``geo`` if you use ```pop_pools`` <#pop_pools>`_/```country_pools`` <#country_pools>`_/```region_pools`` <#region_pools>`_ otherwise ``off``. Available values: ``off``, ``geo``, ``dynamic_latency``, ``random``, ``proximity``, ``""`` Defaults to ``""``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#steering_policy LoadBalancer#steering_policy}
        '''
        result = self._values.get("steering_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''Time to live (TTL) of the DNS entry for the IP address returned by this load balancer.

        This cannot be set for proxied load balancers. Defaults to ``30``. Conflicts with ``proxied``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#ttl LoadBalancer#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerCountryPools",
    jsii_struct_bases=[],
    name_mapping={"country": "country", "pool_ids": "poolIds"},
)
class LoadBalancerCountryPools:
    def __init__(
        self,
        *,
        country: builtins.str,
        pool_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param country: A country code which can be determined with the Load Balancing Regions API described `here <https://developers.cloudflare.com/load-balancing/reference/region-mapping-api/>`_. Multiple entries should not be specified with the same country. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country LoadBalancer#country}
        :param pool_ids: A list of pool IDs in failover priority to use in the given country. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b0daf3d0d177f60400d4a93728ab851bf10622630f28d737aeb8d7c2eee5a7)
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument pool_ids", value=pool_ids, expected_type=type_hints["pool_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "country": country,
            "pool_ids": pool_ids,
        }

    @builtins.property
    def country(self) -> builtins.str:
        '''A country code which can be determined with the Load Balancing Regions API described `here <https://developers.cloudflare.com/load-balancing/reference/region-mapping-api/>`_. Multiple entries should not be specified with the same country.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country LoadBalancer#country}
        '''
        result = self._values.get("country")
        assert result is not None, "Required property 'country' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool_ids(self) -> typing.List[builtins.str]:
        '''A list of pool IDs in failover priority to use in the given country.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        '''
        result = self._values.get("pool_ids")
        assert result is not None, "Required property 'pool_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerCountryPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerCountryPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerCountryPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5548baca517597e80277b08da446c45a8f51631c8e33ff5c8752d5cd3a72440)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerCountryPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee511752c059d5fe31e6576972c7845577edf5266b0034f168b3800e3f8fbd01)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerCountryPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a03adce2efde6f1f00645b6dfcafff0849b9d18ab7b3cab77e5e682f4005551)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0efbe75a11a9650fc79b6553f2273f5c605c08530aeb9cef5a87d1f174689749)
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
            type_hints = typing.get_type_hints(_typecheckingstub__563a476817276bd3c54a24c10e0156f07d9ce998eca4226121fd1890142b75f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerCountryPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerCountryPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerCountryPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35965adf8611b7414765ef01ccff4401c14e6a1c5709fed9b03a5f5b2fa5365f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerCountryPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerCountryPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cdc22231cdd036c54071ec37bf2a65a304f331e649108c1d23d78131b909f14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="poolIdsInput")
    def pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "poolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4ffc12370605081eaf6cca687742727921c5bb1c257d0e045a165a3e0dcf61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value)

    @builtins.property
    @jsii.member(jsii_name="poolIds")
    def pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "poolIds"))

    @pool_ids.setter
    def pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9973ba5fda63b86e30deb7aa8265935a5e08056740c2ac107f00efbb33752d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerCountryPools, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerCountryPools, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerCountryPools, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01fac163181d041e619ec731cf4eb19f20c5da329298ce5b7c00a06db152ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerLocationStrategy",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "prefer_ecs": "preferEcs"},
)
class LoadBalancerLocationStrategy:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        prefer_ecs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Determines the authoritative location when ECS is not preferred, does not exist in the request, or its GeoIP lookup is unsuccessful. Value ``pop`` will use the Cloudflare PoP location. Value ``resolver_ip`` will use the DNS resolver GeoIP location. If the GeoIP lookup is unsuccessful, it will use the Cloudflare PoP location. Available values: ``pop``, ``resolver_ip``. Defaults to ``pop``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#mode LoadBalancer#mode}
        :param prefer_ecs: Whether the EDNS Client Subnet (ECS) GeoIP should be preferred as the authoritative location. Value ``always`` will always prefer ECS, ``never`` will never prefer ECS, ``proximity`` will prefer ECS only when ```steering_policy="proximity"`` <#steering_policy>`_, and ``geo`` will prefer ECS only when ```steering_policy="geo"`` <#steering_policy>`_. Available values: ``always``, ``never``, ``proximity``, ``geo``. Defaults to ``proximity``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#prefer_ecs LoadBalancer#prefer_ecs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d0457eea690b702cd82d00d1d62a0d5a8fe1280f78f5baff5cd4e5a844b3b2)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument prefer_ecs", value=prefer_ecs, expected_type=type_hints["prefer_ecs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if prefer_ecs is not None:
            self._values["prefer_ecs"] = prefer_ecs

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Determines the authoritative location when ECS is not preferred, does not exist in the request, or its GeoIP lookup is unsuccessful.

        Value ``pop`` will use the Cloudflare PoP location. Value ``resolver_ip`` will use the DNS resolver GeoIP location. If the GeoIP lookup is unsuccessful, it will use the Cloudflare PoP location. Available values: ``pop``, ``resolver_ip``. Defaults to ``pop``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#mode LoadBalancer#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefer_ecs(self) -> typing.Optional[builtins.str]:
        '''Whether the EDNS Client Subnet (ECS) GeoIP should be preferred as the authoritative location.

        Value ``always`` will always prefer ECS, ``never`` will never prefer ECS, ``proximity`` will prefer ECS only when ```steering_policy="proximity"`` <#steering_policy>`_, and ``geo`` will prefer ECS only when ```steering_policy="geo"`` <#steering_policy>`_. Available values: ``always``, ``never``, ``proximity``, ``geo``. Defaults to ``proximity``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#prefer_ecs LoadBalancer#prefer_ecs}
        '''
        result = self._values.get("prefer_ecs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerLocationStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerLocationStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerLocationStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3636585e1fd34e70e4640cd6d7be47fd35ff440924016bed9fe10c92d51b817)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerLocationStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91a1e6cdd56a1366dd6120a236bb6b6b78dc2c088b14857cb5f1c5034f8e465)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerLocationStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88f05649b0e15c18d251c96b4d0b365a9e157c8e4d3be62a9f5f18dacfa3a6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53c7b8f18e11daf0cd7927acb2bcf22cff2577b5dbb7bac45a97e2399e468b9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ac9c9a67ee7c88a21e0c107afd4b4a638fba43e06115f10e283c979c4381dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerLocationStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerLocationStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerLocationStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d540ff6c8ed8b8c2ea94bf4fe4b715599536ec4fe37e00eefc7bf0e2401fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerLocationStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerLocationStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e81b5884646eb683c1088e82b1ba373165f971f9550ab7a9950624c0fa774f6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetPreferEcs")
    def reset_prefer_ecs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferEcs", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="preferEcsInput")
    def prefer_ecs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferEcsInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283834d4efe18f2ecca14babcc0cff3cc686560412d787bb702fb0f888ee83e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="preferEcs")
    def prefer_ecs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferEcs"))

    @prefer_ecs.setter
    def prefer_ecs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7502d6738609e16ad083c65590cb0aae8820f91260ffc08dc679caa3a79d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferEcs", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerLocationStrategy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerLocationStrategy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerLocationStrategy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154dac22f09bd45bd574fb93d3a050a49415bdd268301d55ed3771479657a7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerPopPools",
    jsii_struct_bases=[],
    name_mapping={"pool_ids": "poolIds", "pop": "pop"},
)
class LoadBalancerPopPools:
    def __init__(
        self,
        *,
        pool_ids: typing.Sequence[builtins.str],
        pop: builtins.str,
    ) -> None:
        '''
        :param pool_ids: A list of pool IDs in failover priority to use for traffic reaching the given PoP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        :param pop: A 3-letter code for the Point-of-Presence. Allowed values can be found in the list of datacenters on the `status page <https://www.cloudflarestatus.com/>`_. Multiple entries should not be specified with the same PoP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop LoadBalancer#pop}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33959bd2b04d58ab97c408caf9651653bfa0be987b6eab3c6d4421d0fae7f16b)
            check_type(argname="argument pool_ids", value=pool_ids, expected_type=type_hints["pool_ids"])
            check_type(argname="argument pop", value=pop, expected_type=type_hints["pop"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_ids": pool_ids,
            "pop": pop,
        }

    @builtins.property
    def pool_ids(self) -> typing.List[builtins.str]:
        '''A list of pool IDs in failover priority to use for traffic reaching the given PoP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        '''
        result = self._values.get("pool_ids")
        assert result is not None, "Required property 'pool_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def pop(self) -> builtins.str:
        '''A 3-letter code for the Point-of-Presence.

        Allowed values can be found in the list of datacenters on the `status page <https://www.cloudflarestatus.com/>`_. Multiple entries should not be specified with the same PoP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop LoadBalancer#pop}
        '''
        result = self._values.get("pop")
        assert result is not None, "Required property 'pop' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerPopPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerPopPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerPopPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92f89461863299705db1cba4af17061563d33fa656949aac3d70cee1aee04907)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerPopPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eed29d5ce9b0e646119d2e53c5d8122e9118aa76be22a1b2925e3452f9dd2ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerPopPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd5176f46154ebbc237ceec96c7d6ed2e3a76b54c718b6a738a8e68080c6e80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bddeb513de7b059571c8bd61ba7c4b4922f85ff1f7f7d3291be043ddc56bbf91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b27c390956528201cd3f387829ec0a2eb4613290f074be0d213875f77e8f1cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPopPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPopPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPopPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5959a17b4c9e55b6dbdf79ee4a421978077f003a69dc25996b54cd9010d0b7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerPopPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerPopPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e84781d122a88e5c575953503e586a779f2a1548efff52d90cf2e043733f8ee4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="poolIdsInput")
    def pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "poolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="popInput")
    def pop_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "popInput"))

    @builtins.property
    @jsii.member(jsii_name="poolIds")
    def pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "poolIds"))

    @pool_ids.setter
    def pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208ab23cda9b812c72e86ae04ee2ce9ce7a25fbfab670853bddc25cc2da49031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolIds", value)

    @builtins.property
    @jsii.member(jsii_name="pop")
    def pop(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pop"))

    @pop.setter
    def pop(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d031cac610c522a5f74485725bcc2f4f29fef327e00a75a8c27eaa604b1f0134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pop", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerPopPools, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerPopPools, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerPopPools, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672260e434f5c32d7753e04817acb246b7c4d746aaf1c7b5d96f07e0378361c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRandomSteering",
    jsii_struct_bases=[],
    name_mapping={"default_weight": "defaultWeight", "pool_weights": "poolWeights"},
)
class LoadBalancerRandomSteering:
    def __init__(
        self,
        *,
        default_weight: typing.Optional[jsii.Number] = None,
        pool_weights: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
    ) -> None:
        '''
        :param default_weight: The default weight for pools in the load balancer that are not specified in the ```pool_weights`` <#pool_weights>`_ map. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_weight LoadBalancer#default_weight}
        :param pool_weights: A mapping of pool IDs to custom weights. The weight is relative to other pools in the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_weights LoadBalancer#pool_weights}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee03b4afc82f161efabb876910cdab21e26982c73d8eef161bdf1806f028519b)
            check_type(argname="argument default_weight", value=default_weight, expected_type=type_hints["default_weight"])
            check_type(argname="argument pool_weights", value=pool_weights, expected_type=type_hints["pool_weights"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_weight is not None:
            self._values["default_weight"] = default_weight
        if pool_weights is not None:
            self._values["pool_weights"] = pool_weights

    @builtins.property
    def default_weight(self) -> typing.Optional[jsii.Number]:
        '''The default weight for pools in the load balancer that are not specified in the ```pool_weights`` <#pool_weights>`_ map.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_weight LoadBalancer#default_weight}
        '''
        result = self._values.get("default_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pool_weights(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        '''A mapping of pool IDs to custom weights. The weight is relative to other pools in the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_weights LoadBalancer#pool_weights}
        '''
        result = self._values.get("pool_weights")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRandomSteering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRandomSteeringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRandomSteeringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__632645b91a77660587cbc1ba26291b0820892ad8d8dbc3908e74e4b5d1bc6a33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerRandomSteeringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49754c2b67088eb68cf724681fa4f887bfc9718dec179e0c0717c8606db04d19)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRandomSteeringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e60d66fc66b196b3d04a3274188d99a230d055956f2146b5dba2b3edebc57f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be22d3daddfdb6dabb2258f4252ae26ba0c8f73f9df7b460a2fc1087dc2d60b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9e7502eed605864fe5c76fa994a54205d98b918c73fdf639a34f00ee468be6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRandomSteering]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRandomSteering]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRandomSteering]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5790f54b965a1b90119a410dcd2a92db95e4b443668c1955188310c5e89b50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRandomSteeringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRandomSteeringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eff3856a00584fdf493670649b9ffda272af232d2ba2774e2a2317ee7892ea4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDefaultWeight")
    def reset_default_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultWeight", []))

    @jsii.member(jsii_name="resetPoolWeights")
    def reset_pool_weights(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPoolWeights", []))

    @builtins.property
    @jsii.member(jsii_name="defaultWeightInput")
    def default_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="poolWeightsInput")
    def pool_weights_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], jsii.get(self, "poolWeightsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultWeight")
    def default_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultWeight"))

    @default_weight.setter
    def default_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64146deae2c3ed36b3305117fa981b5b7c9a1164677f036cb508f162493c0086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultWeight", value)

    @builtins.property
    @jsii.member(jsii_name="poolWeights")
    def pool_weights(self) -> typing.Mapping[builtins.str, jsii.Number]:
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "poolWeights"))

    @pool_weights.setter
    def pool_weights(self, value: typing.Mapping[builtins.str, jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9973a0c91cce2364e7bca20eead582d2bb02780a7f8a4182cefbd38c49d0b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolWeights", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRandomSteering, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRandomSteering, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRandomSteering, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aecaf7995fee6243343cf4dfffae58904bdf43c75cc42227c30cfacfa4083ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRegionPools",
    jsii_struct_bases=[],
    name_mapping={"pool_ids": "poolIds", "region": "region"},
)
class LoadBalancerRegionPools:
    def __init__(
        self,
        *,
        pool_ids: typing.Sequence[builtins.str],
        region: builtins.str,
    ) -> None:
        '''
        :param pool_ids: A list of pool IDs in failover priority to use in the given region. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        :param region: A region code which must be in the list defined `here <https://developers.cloudflare.com/load-balancing/reference/region-mapping-api/#list-of-load-balancer-regions>`_. Multiple entries should not be specified with the same region. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region LoadBalancer#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c8d4144cb636bf8b01cfe1d17204a0016b1c54e821d1f4c5b79a10641db53e)
            check_type(argname="argument pool_ids", value=pool_ids, expected_type=type_hints["pool_ids"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_ids": pool_ids,
            "region": region,
        }

    @builtins.property
    def pool_ids(self) -> typing.List[builtins.str]:
        '''A list of pool IDs in failover priority to use in the given region.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        '''
        result = self._values.get("pool_ids")
        assert result is not None, "Required property 'pool_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def region(self) -> builtins.str:
        '''A region code which must be in the list defined `here <https://developers.cloudflare.com/load-balancing/reference/region-mapping-api/#list-of-load-balancer-regions>`_. Multiple entries should not be specified with the same region.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region LoadBalancer#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRegionPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRegionPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRegionPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6e6663dfe2a4a8c169517bbd45c29fc6c961e6d87abdb4f554e078842efec25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerRegionPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1b1d353584d0e935cad04a58df6efe2914c1184a0672c1855bcaa81df914f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRegionPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aed4140b729002e0421cc7fd26ac7935f4eff3666b8879b389b3d4812899a15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a562f6de04282898ce16a3544850b17d09b0a70b13f9dfc8fc0e4ddfe1f9c2aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb91ea7c56abd8721824126b4b32b96e04867762adffd58552d4ba63d522050b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRegionPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRegionPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRegionPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d086972694af7ebbf3146f856de93494d223c98382d014300f4d0779172131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRegionPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRegionPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e61aa2c8772eb177ee7c1aeeb0e613107818a4c08aeecc835d33f3b759978751)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="poolIdsInput")
    def pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "poolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="poolIds")
    def pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "poolIds"))

    @pool_ids.setter
    def pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ed2ab576dea8049ab36066f6772645f3f6529e8316e192ed60fbd31efd8b48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolIds", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e4773fde1a9c08d688e3199f0a5242863d3965d7005829cbb249f47f053c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRegionPools, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRegionPools, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRegionPools, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dbf6c2b118bdc11525d869dfec93cdf977ff48aa452e66e94599e2bb880e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRules",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "condition": "condition",
        "disabled": "disabled",
        "fixed_response": "fixedResponse",
        "overrides": "overrides",
        "priority": "priority",
        "terminates": "terminates",
    },
)
class LoadBalancerRules:
    def __init__(
        self,
        *,
        name: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fixed_response: typing.Optional[typing.Union["LoadBalancerRulesFixedResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        terminates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Human readable name for this rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#name LoadBalancer#name}
        :param condition: The statement to evaluate to determine if this rule's effects should be applied. An empty condition is always true. See `load balancing rules <https://developers.cloudflare.com/load-balancing/understand-basics/load-balancing-rules>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#condition LoadBalancer#condition}
        :param disabled: A disabled rule will not be executed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#disabled LoadBalancer#disabled}
        :param fixed_response: fixed_response block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#fixed_response LoadBalancer#fixed_response}
        :param overrides: overrides block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#overrides LoadBalancer#overrides}
        :param priority: Priority used when determining the order of rule execution. Lower values are executed first. If not provided, the list order will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#priority LoadBalancer#priority}
        :param terminates: Terminates indicates that if this rule is true no further rules should be executed. Note: setting a ```fixed_response`` <#fixed_response>`_ forces this field to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#terminates LoadBalancer#terminates}
        '''
        if isinstance(fixed_response, dict):
            fixed_response = LoadBalancerRulesFixedResponse(**fixed_response)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fdf42061a6652ffd6986a8e2ec9edad4427316f2d7a2321fe44f8214e666716)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument fixed_response", value=fixed_response, expected_type=type_hints["fixed_response"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument terminates", value=terminates, expected_type=type_hints["terminates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if condition is not None:
            self._values["condition"] = condition
        if disabled is not None:
            self._values["disabled"] = disabled
        if fixed_response is not None:
            self._values["fixed_response"] = fixed_response
        if overrides is not None:
            self._values["overrides"] = overrides
        if priority is not None:
            self._values["priority"] = priority
        if terminates is not None:
            self._values["terminates"] = terminates

    @builtins.property
    def name(self) -> builtins.str:
        '''Human readable name for this rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#name LoadBalancer#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''The statement to evaluate to determine if this rule's effects should be applied.

        An empty condition is always true. See `load balancing rules <https://developers.cloudflare.com/load-balancing/understand-basics/load-balancing-rules>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#condition LoadBalancer#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A disabled rule will not be executed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#disabled LoadBalancer#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fixed_response(self) -> typing.Optional["LoadBalancerRulesFixedResponse"]:
        '''fixed_response block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#fixed_response LoadBalancer#fixed_response}
        '''
        result = self._values.get("fixed_response")
        return typing.cast(typing.Optional["LoadBalancerRulesFixedResponse"], result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverrides"]]]:
        '''overrides block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#overrides LoadBalancer#overrides}
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverrides"]]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Priority used when determining the order of rule execution.

        Lower values are executed first. If not provided, the list order will be used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#priority LoadBalancer#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def terminates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Terminates indicates that if this rule is true no further rules should be executed.

        Note: setting a ```fixed_response`` <#fixed_response>`_ forces this field to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#terminates LoadBalancer#terminates}
        '''
        result = self._values.get("terminates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesFixedResponse",
    jsii_struct_bases=[],
    name_mapping={
        "content_type": "contentType",
        "location": "location",
        "message_body": "messageBody",
        "status_code": "statusCode",
    },
)
class LoadBalancerRulesFixedResponse:
    def __init__(
        self,
        *,
        content_type: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        message_body: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param content_type: The value of the HTTP context-type header for this fixed response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#content_type LoadBalancer#content_type}
        :param location: The value of the HTTP location header for this fixed response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#location LoadBalancer#location}
        :param message_body: The text used as the html body for this fixed response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#message_body LoadBalancer#message_body}
        :param status_code: The HTTP status code used for this fixed response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#status_code LoadBalancer#status_code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06a358aa30363c798305232d6e623350e1f1c44109315e688dbf167c0529967)
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument message_body", value=message_body, expected_type=type_hints["message_body"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_type is not None:
            self._values["content_type"] = content_type
        if location is not None:
            self._values["location"] = location
        if message_body is not None:
            self._values["message_body"] = message_body
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''The value of the HTTP context-type header for this fixed response.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#content_type LoadBalancer#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The value of the HTTP location header for this fixed response.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#location LoadBalancer#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_body(self) -> typing.Optional[builtins.str]:
        '''The text used as the html body for this fixed response.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#message_body LoadBalancer#message_body}
        '''
        result = self._values.get("message_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_code(self) -> typing.Optional[jsii.Number]:
        '''The HTTP status code used for this fixed response.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#status_code LoadBalancer#status_code}
        '''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRulesFixedResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRulesFixedResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesFixedResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80108d9aa8c23f36e4b7063ba0aa4b31c3e1275949022514800f4c8eb0d14916)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMessageBody")
    def reset_message_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageBody", []))

    @jsii.member(jsii_name="resetStatusCode")
    def reset_status_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusCode", []))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="messageBodyInput")
    def message_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86270d9848d23db8e4200b0e35ebc9fc45e5da1d517d6a31bc7780f890383a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b015c6e42a266873f9a700c8a31631697378013d1c81a51f6dee7696471a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="messageBody")
    def message_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageBody"))

    @message_body.setter
    def message_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69434f811e173e46da313f9aedd1026400d0a3b9a0174f3f0300bfbc6774e9f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageBody", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf77b24367c791875e918c3a9cedf3f2147f45e4dacbb0aeb750962fad39bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LoadBalancerRulesFixedResponse]:
        return typing.cast(typing.Optional[LoadBalancerRulesFixedResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LoadBalancerRulesFixedResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1307772712904f3a25b1d8ff5167a3a18cacea694ac2ce73bd9c48607726e4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59baa239d8e3ea247aac1525b719e2de365c0547c13a6e6738e91104b679e18f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd5d663b462645948272bde24a3e6a192a833e4d72fadcfbe9d26e8affa9a19)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd04c38c24c581759071ae44418fc173fd284b9cd0edbbd2f85e435c9c1c578)
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
            type_hints = typing.get_type_hints(_typecheckingstub__521357c4039603ba4551315908639be87cc4d2d45ba7c9ab2982e88e9e19fe09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3db24e37e9660436ce55e2591e403ae318662c1893aea722586425995eeb689f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2aab7db6cb77dc7546b011c288f299e644f90b4e6681a5fadb150655069bd9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeb822e0195a87da51205f90f18bdae2e8a011b0c0b8be0a23f2767a53a54c34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFixedResponse")
    def put_fixed_response(
        self,
        *,
        content_type: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        message_body: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param content_type: The value of the HTTP context-type header for this fixed response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#content_type LoadBalancer#content_type}
        :param location: The value of the HTTP location header for this fixed response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#location LoadBalancer#location}
        :param message_body: The text used as the html body for this fixed response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#message_body LoadBalancer#message_body}
        :param status_code: The HTTP status code used for this fixed response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#status_code LoadBalancer#status_code}
        '''
        value = LoadBalancerRulesFixedResponse(
            content_type=content_type,
            location=location,
            message_body=message_body,
            status_code=status_code,
        )

        return typing.cast(None, jsii.invoke(self, "putFixedResponse", [value]))

    @jsii.member(jsii_name="putOverrides")
    def put_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1128822e7fffe327616b8160ad4df31c1407481a501f919f59f92034cee83171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOverrides", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetFixedResponse")
    def reset_fixed_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedResponse", []))

    @jsii.member(jsii_name="resetOverrides")
    def reset_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrides", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetTerminates")
    def reset_terminates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminates", []))

    @builtins.property
    @jsii.member(jsii_name="fixedResponse")
    def fixed_response(self) -> LoadBalancerRulesFixedResponseOutputReference:
        return typing.cast(LoadBalancerRulesFixedResponseOutputReference, jsii.get(self, "fixedResponse"))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> "LoadBalancerRulesOverridesList":
        return typing.cast("LoadBalancerRulesOverridesList", jsii.get(self, "overrides"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedResponseInput")
    def fixed_response_input(self) -> typing.Optional[LoadBalancerRulesFixedResponse]:
        return typing.cast(typing.Optional[LoadBalancerRulesFixedResponse], jsii.get(self, "fixedResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overridesInput")
    def overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverrides"]]], jsii.get(self, "overridesInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="terminatesInput")
    def terminates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "terminatesInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc94eb429048c5fdcba032f9097bff452e96a8b87a21ed14207910ff9ebd8e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value)

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970524bed5e99690908d85d4d7ac78a7ba44a085d24880cb72687193e0e9bc09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7098ca56037e693d628373e3a6f18993274641304d612d1ad77069af9d82e1ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3294de3d4a5c794f3bceef16b338e69245d8e1474e2ca04d3e6c6914850bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="terminates")
    def terminates(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "terminates"))

    @terminates.setter
    def terminates(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66223bd8cfe2d18c3c9439fce67488c94926fc3e7f8f4f9a245979aa2a5bdce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminates", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRules, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRules, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRules, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be777163ff6c1b6b7d0e9fbbc7f8a8d9c7d76e6976ca4eeac1712b453685526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "adaptive_routing": "adaptiveRouting",
        "country_pools": "countryPools",
        "default_pools": "defaultPools",
        "fallback_pool": "fallbackPool",
        "location_strategy": "locationStrategy",
        "pop_pools": "popPools",
        "random_steering": "randomSteering",
        "region_pools": "regionPools",
        "session_affinity": "sessionAffinity",
        "session_affinity_attributes": "sessionAffinityAttributes",
        "session_affinity_ttl": "sessionAffinityTtl",
        "steering_policy": "steeringPolicy",
        "ttl": "ttl",
    },
)
class LoadBalancerRulesOverrides:
    def __init__(
        self,
        *,
        adaptive_routing: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesAdaptiveRouting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        country_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesCountryPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        fallback_pool: typing.Optional[builtins.str] = None,
        location_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesLocationStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pop_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesPopPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        random_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesRandomSteering", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesRegionPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        session_affinity_ttl: typing.Optional[jsii.Number] = None,
        steering_policy: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param adaptive_routing: adaptive_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#adaptive_routing LoadBalancer#adaptive_routing}
        :param country_pools: country_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country_pools LoadBalancer#country_pools}
        :param default_pools: See ```default_pool_ids`` <#default_pool_ids>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_pools LoadBalancer#default_pools}
        :param fallback_pool: See ```fallback_pool_id`` <#fallback_pool_id>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#fallback_pool LoadBalancer#fallback_pool}
        :param location_strategy: location_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#location_strategy LoadBalancer#location_strategy}
        :param pop_pools: pop_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop_pools LoadBalancer#pop_pools}
        :param random_steering: random_steering block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#random_steering LoadBalancer#random_steering}
        :param region_pools: region_pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region_pools LoadBalancer#region_pools}
        :param session_affinity: See ```session_affinity`` <#session_affinity>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity LoadBalancer#session_affinity}
        :param session_affinity_attributes: See ```session_affinity_attributes`` <#nested-schema-for-session_affinity_attributes>`_. Note that the property ```drain_duration`` <#drain_duration>`_ is not currently supported as a rule override. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_attributes LoadBalancer#session_affinity_attributes}
        :param session_affinity_ttl: See ```session_affinity_ttl`` <#session_affinity_ttl>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_ttl LoadBalancer#session_affinity_ttl}
        :param steering_policy: See ```steering_policy`` <#steering_policy>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#steering_policy LoadBalancer#steering_policy}
        :param ttl: See ```ttl`` <#ttl>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#ttl LoadBalancer#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f9ec836d04efd6df32310c87de2c9677c1832a61280179f4a5f5628a3a2bdc)
            check_type(argname="argument adaptive_routing", value=adaptive_routing, expected_type=type_hints["adaptive_routing"])
            check_type(argname="argument country_pools", value=country_pools, expected_type=type_hints["country_pools"])
            check_type(argname="argument default_pools", value=default_pools, expected_type=type_hints["default_pools"])
            check_type(argname="argument fallback_pool", value=fallback_pool, expected_type=type_hints["fallback_pool"])
            check_type(argname="argument location_strategy", value=location_strategy, expected_type=type_hints["location_strategy"])
            check_type(argname="argument pop_pools", value=pop_pools, expected_type=type_hints["pop_pools"])
            check_type(argname="argument random_steering", value=random_steering, expected_type=type_hints["random_steering"])
            check_type(argname="argument region_pools", value=region_pools, expected_type=type_hints["region_pools"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument session_affinity_attributes", value=session_affinity_attributes, expected_type=type_hints["session_affinity_attributes"])
            check_type(argname="argument session_affinity_ttl", value=session_affinity_ttl, expected_type=type_hints["session_affinity_ttl"])
            check_type(argname="argument steering_policy", value=steering_policy, expected_type=type_hints["steering_policy"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if adaptive_routing is not None:
            self._values["adaptive_routing"] = adaptive_routing
        if country_pools is not None:
            self._values["country_pools"] = country_pools
        if default_pools is not None:
            self._values["default_pools"] = default_pools
        if fallback_pool is not None:
            self._values["fallback_pool"] = fallback_pool
        if location_strategy is not None:
            self._values["location_strategy"] = location_strategy
        if pop_pools is not None:
            self._values["pop_pools"] = pop_pools
        if random_steering is not None:
            self._values["random_steering"] = random_steering
        if region_pools is not None:
            self._values["region_pools"] = region_pools
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if session_affinity_attributes is not None:
            self._values["session_affinity_attributes"] = session_affinity_attributes
        if session_affinity_ttl is not None:
            self._values["session_affinity_ttl"] = session_affinity_ttl
        if steering_policy is not None:
            self._values["steering_policy"] = steering_policy
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def adaptive_routing(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesAdaptiveRouting"]]]:
        '''adaptive_routing block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#adaptive_routing LoadBalancer#adaptive_routing}
        '''
        result = self._values.get("adaptive_routing")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesAdaptiveRouting"]]], result)

    @builtins.property
    def country_pools(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesCountryPools"]]]:
        '''country_pools block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country_pools LoadBalancer#country_pools}
        '''
        result = self._values.get("country_pools")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesCountryPools"]]], result)

    @builtins.property
    def default_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''See ```default_pool_ids`` <#default_pool_ids>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_pools LoadBalancer#default_pools}
        '''
        result = self._values.get("default_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fallback_pool(self) -> typing.Optional[builtins.str]:
        '''See ```fallback_pool_id`` <#fallback_pool_id>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#fallback_pool LoadBalancer#fallback_pool}
        '''
        result = self._values.get("fallback_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesLocationStrategy"]]]:
        '''location_strategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#location_strategy LoadBalancer#location_strategy}
        '''
        result = self._values.get("location_strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesLocationStrategy"]]], result)

    @builtins.property
    def pop_pools(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesPopPools"]]]:
        '''pop_pools block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop_pools LoadBalancer#pop_pools}
        '''
        result = self._values.get("pop_pools")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesPopPools"]]], result)

    @builtins.property
    def random_steering(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesRandomSteering"]]]:
        '''random_steering block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#random_steering LoadBalancer#random_steering}
        '''
        result = self._values.get("random_steering")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesRandomSteering"]]], result)

    @builtins.property
    def region_pools(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesRegionPools"]]]:
        '''region_pools block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region_pools LoadBalancer#region_pools}
        '''
        result = self._values.get("region_pools")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesRegionPools"]]], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''See ```session_affinity`` <#session_affinity>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity LoadBalancer#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''See ```session_affinity_attributes`` <#nested-schema-for-session_affinity_attributes>`_. Note that the property ```drain_duration`` <#drain_duration>`_ is not currently supported as a rule override.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_attributes LoadBalancer#session_affinity_attributes}
        '''
        result = self._values.get("session_affinity_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def session_affinity_ttl(self) -> typing.Optional[jsii.Number]:
        '''See ```session_affinity_ttl`` <#session_affinity_ttl>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#session_affinity_ttl LoadBalancer#session_affinity_ttl}
        '''
        result = self._values.get("session_affinity_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def steering_policy(self) -> typing.Optional[builtins.str]:
        '''See ```steering_policy`` <#steering_policy>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#steering_policy LoadBalancer#steering_policy}
        '''
        result = self._values.get("steering_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''See ```ttl`` <#ttl>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#ttl LoadBalancer#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRulesOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesAdaptiveRouting",
    jsii_struct_bases=[],
    name_mapping={"failover_across_pools": "failoverAcrossPools"},
)
class LoadBalancerRulesOverridesAdaptiveRouting:
    def __init__(
        self,
        *,
        failover_across_pools: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param failover_across_pools: See ```failover_across_pools`` <#failover_across_pools>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#failover_across_pools LoadBalancer#failover_across_pools}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e2e8cb8e4a79360b5de5e2325232e4c6100f6a32a2ab352bcb66c2d74ad625)
            check_type(argname="argument failover_across_pools", value=failover_across_pools, expected_type=type_hints["failover_across_pools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failover_across_pools is not None:
            self._values["failover_across_pools"] = failover_across_pools

    @builtins.property
    def failover_across_pools(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''See ```failover_across_pools`` <#failover_across_pools>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#failover_across_pools LoadBalancer#failover_across_pools}
        '''
        result = self._values.get("failover_across_pools")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRulesOverridesAdaptiveRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRulesOverridesAdaptiveRoutingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesAdaptiveRoutingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe8b3e5b80047cb5c9976482c22083a7597952c88d6940a50955f79e33844b48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoadBalancerRulesOverridesAdaptiveRoutingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570bc537028c697b0d4d1377f495366a2c4317e9105e963853a68b707b4629dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRulesOverridesAdaptiveRoutingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df15b04ba4fc8c8cc34c3e3f41374780eeb0c45877d65c567120155c3fd8ebd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3bbd90daa4fdd900e3fdff88bbfc460f38e4a288a2b7629a481ac391b89381f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6667d3650106a5eaeca757c9e1f029bd6f17994ed158e101a290c18ed2eb8ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesAdaptiveRouting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesAdaptiveRouting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesAdaptiveRouting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2747a5877a5ba632852ba597a7c003924ec2855f4b0f20981ddb4f8588893050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOverridesAdaptiveRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesAdaptiveRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a7efd7e78658287b28e5ba6c9d99fd5f22803fb81fd0c9a750d67e5c32faa5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFailoverAcrossPools")
    def reset_failover_across_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverAcrossPools", []))

    @builtins.property
    @jsii.member(jsii_name="failoverAcrossPoolsInput")
    def failover_across_pools_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failoverAcrossPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverAcrossPools")
    def failover_across_pools(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failoverAcrossPools"))

    @failover_across_pools.setter
    def failover_across_pools(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba808bf362e4eba92256ff998ed3db7c2a9341a8469fb85e0563777f8442a0f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverAcrossPools", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRulesOverridesAdaptiveRouting, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRulesOverridesAdaptiveRouting, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRulesOverridesAdaptiveRouting, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacd7002058763798e137aaa37b1041267fb13953033e1caaf6edee7a3356bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesCountryPools",
    jsii_struct_bases=[],
    name_mapping={"country": "country", "pool_ids": "poolIds"},
)
class LoadBalancerRulesOverridesCountryPools:
    def __init__(
        self,
        *,
        country: builtins.str,
        pool_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param country: See ```country`` <#country>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country LoadBalancer#country}
        :param pool_ids: See ```pool_ids`` <#pool_ids>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd268733c4bc495a9fc0207b00546529b5588c4377ee5d92d1460d51d8aca7a8)
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument pool_ids", value=pool_ids, expected_type=type_hints["pool_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "country": country,
            "pool_ids": pool_ids,
        }

    @builtins.property
    def country(self) -> builtins.str:
        '''See ```country`` <#country>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#country LoadBalancer#country}
        '''
        result = self._values.get("country")
        assert result is not None, "Required property 'country' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool_ids(self) -> typing.List[builtins.str]:
        '''See ```pool_ids`` <#pool_ids>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        '''
        result = self._values.get("pool_ids")
        assert result is not None, "Required property 'pool_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRulesOverridesCountryPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRulesOverridesCountryPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesCountryPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f68f1ce3ce85a721c6987514ea6f744969031db22026dcba02cf404e7a57f320)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoadBalancerRulesOverridesCountryPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52610fc2d63e239a20114270ede8042b2be3c39e7506d36782c9d5f808c5f359)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRulesOverridesCountryPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ccd859b55a9e20f703ff1f1605dfaa1bc099b8d4c303efe0dfa47461e1b2478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bb389ca7c85f896b516017288618048963ebbf4d5abe8c69c0b45fd04ad0410)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6b6517e781dbd2d2c0e11fd980c17688bd45e4422a433b40e74c4c395f3ada1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesCountryPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesCountryPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesCountryPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64b0a55f0a7c206e1f2a0ebf5e7fa3c88c08fc5c1f1a7f45f2160841e5fd776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOverridesCountryPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesCountryPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af5414311dbda1ee3a2f6f5e125a1421117934b111d152fabcad27eb8f936b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="poolIdsInput")
    def pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "poolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a2867eb44234989b462c76861e6e3b7197c18f84e2c0e4f08137f20a7a7227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value)

    @builtins.property
    @jsii.member(jsii_name="poolIds")
    def pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "poolIds"))

    @pool_ids.setter
    def pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e663f2de378a95564859a1574956f2326064841d42b13aa3d78dcbb26ddf0bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRulesOverridesCountryPools, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRulesOverridesCountryPools, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRulesOverridesCountryPools, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e3f7bf2f9e3bdb8cc5e57d5fc525d0ecc208ebfa5bac859004c59e8a1f981c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18fe80b59272da0ca21b3486df6e040943336c01fc85eb15870b312b293fe8aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerRulesOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d90b4c69a4eda8f37e43836fa234cbe4c1624bef4d909dbffb193e52186af67)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRulesOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7adfb9f90bd97359ccd54defbd20e2f75fbb0d8c4e8ed595d8a7ffd1b67ca1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2b6e6fe9ee2f96215beef92deb67164a373407cc3674f438ec297a7ff9881ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b2f5819aae0177d2bbeac41763bfb844aedce6524d21217dcbb672200bcecb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7619d73070d4f912d64e6909f2709aa21c67ecc5c86eae5592d9f048ff0dc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesLocationStrategy",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "prefer_ecs": "preferEcs"},
)
class LoadBalancerRulesOverridesLocationStrategy:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        prefer_ecs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: See ```mode`` <#mode>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#mode LoadBalancer#mode}
        :param prefer_ecs: See ```prefer_ecs`` <#prefer_ecs>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#prefer_ecs LoadBalancer#prefer_ecs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7071e21700e31fa074b8b5a8eaf06b619702a637def0209b2bdd1687d7355b4d)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument prefer_ecs", value=prefer_ecs, expected_type=type_hints["prefer_ecs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if prefer_ecs is not None:
            self._values["prefer_ecs"] = prefer_ecs

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''See ```mode`` <#mode>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#mode LoadBalancer#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefer_ecs(self) -> typing.Optional[builtins.str]:
        '''See ```prefer_ecs`` <#prefer_ecs>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#prefer_ecs LoadBalancer#prefer_ecs}
        '''
        result = self._values.get("prefer_ecs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRulesOverridesLocationStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRulesOverridesLocationStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesLocationStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86e88c5a0246cca43aa487213704888993206b309da6e67f41418d6035746998)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoadBalancerRulesOverridesLocationStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62fc10eeb62aac0ce3f9fb31b3fc779a921cf7411cb8c77b8f9bdb3603fe0215)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRulesOverridesLocationStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53eb57e34490025a67c8a9373fb209a9df76a132f2d7be2f100a68245c8d7f0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b65ae2a0783d3cade92ed09359597e8e0a8c04afc44ec2bc144b5108c8c10e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7ebb525e7fa445afd391826eee32224f7aa03721b387679d473f06cef1dc94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesLocationStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesLocationStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesLocationStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825eeb81e2bc1b86f9b554bff0d78c03113e4146bb55ee6fdbaf83c5b0a54ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOverridesLocationStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesLocationStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30a0b307a30466237be574a87cdd5702cd9422a2a7e41360c7c9d139a12a13e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetPreferEcs")
    def reset_prefer_ecs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferEcs", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="preferEcsInput")
    def prefer_ecs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferEcsInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13fca12df2c10577502f0351db487d810d4b94dc8597c923a699d999c6fd7a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="preferEcs")
    def prefer_ecs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferEcs"))

    @prefer_ecs.setter
    def prefer_ecs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7707eb1046a2a52ab76b39bfc611852997beee3f5cdb6c4daaa504f72a21bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferEcs", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRulesOverridesLocationStrategy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRulesOverridesLocationStrategy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRulesOverridesLocationStrategy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41515753604db88b8a568c09f635d7871ab23948ab008963bb5bd6b91a07c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6e3db2746899b32772fe9f12603f7f273304443e2cde098ff2fb855c3740b76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAdaptiveRouting")
    def put_adaptive_routing(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesAdaptiveRouting, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9708d8bd193f530f009e042f15882c02f8056700b0642dd2abefd700d12e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdaptiveRouting", [value]))

    @jsii.member(jsii_name="putCountryPools")
    def put_country_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesCountryPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c0ffa07868d796a1d914c5ed8b779cabfde4d7f527fbf0efbdacd9e3a88ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCountryPools", [value]))

    @jsii.member(jsii_name="putLocationStrategy")
    def put_location_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesLocationStrategy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831f41ebcc9b91a9de41e35f12b1c897ad9cc07c119ff11f950d724081314481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocationStrategy", [value]))

    @jsii.member(jsii_name="putPopPools")
    def put_pop_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesPopPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ffddd4d0e832c5b8e2916c3fca7480aa774d9519356bc045263f4e10269f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPopPools", [value]))

    @jsii.member(jsii_name="putRandomSteering")
    def put_random_steering(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesRandomSteering", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4882363e961f3c6242cbee0b4644c626fe313c4a1d0e9e154661d63345fa08b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRandomSteering", [value]))

    @jsii.member(jsii_name="putRegionPools")
    def put_region_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerRulesOverridesRegionPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3bab50d248c46cc9750589d219f3f105eda534c26bebd16f774ff2fcf46597c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegionPools", [value]))

    @jsii.member(jsii_name="resetAdaptiveRouting")
    def reset_adaptive_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdaptiveRouting", []))

    @jsii.member(jsii_name="resetCountryPools")
    def reset_country_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryPools", []))

    @jsii.member(jsii_name="resetDefaultPools")
    def reset_default_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPools", []))

    @jsii.member(jsii_name="resetFallbackPool")
    def reset_fallback_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFallbackPool", []))

    @jsii.member(jsii_name="resetLocationStrategy")
    def reset_location_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationStrategy", []))

    @jsii.member(jsii_name="resetPopPools")
    def reset_pop_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPopPools", []))

    @jsii.member(jsii_name="resetRandomSteering")
    def reset_random_steering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRandomSteering", []))

    @jsii.member(jsii_name="resetRegionPools")
    def reset_region_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionPools", []))

    @jsii.member(jsii_name="resetSessionAffinity")
    def reset_session_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinity", []))

    @jsii.member(jsii_name="resetSessionAffinityAttributes")
    def reset_session_affinity_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinityAttributes", []))

    @jsii.member(jsii_name="resetSessionAffinityTtl")
    def reset_session_affinity_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinityTtl", []))

    @jsii.member(jsii_name="resetSteeringPolicy")
    def reset_steering_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSteeringPolicy", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @builtins.property
    @jsii.member(jsii_name="adaptiveRouting")
    def adaptive_routing(self) -> LoadBalancerRulesOverridesAdaptiveRoutingList:
        return typing.cast(LoadBalancerRulesOverridesAdaptiveRoutingList, jsii.get(self, "adaptiveRouting"))

    @builtins.property
    @jsii.member(jsii_name="countryPools")
    def country_pools(self) -> LoadBalancerRulesOverridesCountryPoolsList:
        return typing.cast(LoadBalancerRulesOverridesCountryPoolsList, jsii.get(self, "countryPools"))

    @builtins.property
    @jsii.member(jsii_name="locationStrategy")
    def location_strategy(self) -> LoadBalancerRulesOverridesLocationStrategyList:
        return typing.cast(LoadBalancerRulesOverridesLocationStrategyList, jsii.get(self, "locationStrategy"))

    @builtins.property
    @jsii.member(jsii_name="popPools")
    def pop_pools(self) -> "LoadBalancerRulesOverridesPopPoolsList":
        return typing.cast("LoadBalancerRulesOverridesPopPoolsList", jsii.get(self, "popPools"))

    @builtins.property
    @jsii.member(jsii_name="randomSteering")
    def random_steering(self) -> "LoadBalancerRulesOverridesRandomSteeringList":
        return typing.cast("LoadBalancerRulesOverridesRandomSteeringList", jsii.get(self, "randomSteering"))

    @builtins.property
    @jsii.member(jsii_name="regionPools")
    def region_pools(self) -> "LoadBalancerRulesOverridesRegionPoolsList":
        return typing.cast("LoadBalancerRulesOverridesRegionPoolsList", jsii.get(self, "regionPools"))

    @builtins.property
    @jsii.member(jsii_name="adaptiveRoutingInput")
    def adaptive_routing_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesAdaptiveRouting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesAdaptiveRouting]]], jsii.get(self, "adaptiveRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="countryPoolsInput")
    def country_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesCountryPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesCountryPools]]], jsii.get(self, "countryPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPoolsInput")
    def default_pools_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "defaultPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackPoolInput")
    def fallback_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fallbackPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="locationStrategyInput")
    def location_strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesLocationStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesLocationStrategy]]], jsii.get(self, "locationStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="popPoolsInput")
    def pop_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesPopPools"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesPopPools"]]], jsii.get(self, "popPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="randomSteeringInput")
    def random_steering_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesRandomSteering"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesRandomSteering"]]], jsii.get(self, "randomSteeringInput"))

    @builtins.property
    @jsii.member(jsii_name="regionPoolsInput")
    def region_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesRegionPools"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerRulesOverridesRegionPools"]]], jsii.get(self, "regionPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityAttributesInput")
    def session_affinity_attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sessionAffinityAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityTtlInput")
    def session_affinity_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionAffinityTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="steeringPolicyInput")
    def steering_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "steeringPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPools")
    def default_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultPools"))

    @default_pools.setter
    def default_pools(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b23a730bb6221ed135022ddefe56c86eb339adfcc39f52819954e7fa4ab46b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPools", value)

    @builtins.property
    @jsii.member(jsii_name="fallbackPool")
    def fallback_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fallbackPool"))

    @fallback_pool.setter
    def fallback_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87420889d83d51684a80a5b6b9732740355fca6a277bd0004154f57e679dfab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fallbackPool", value)

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2135424592a76b8f56aebfbdbd15a33640fb261375c502e64873fae4cbbb98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value)

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityAttributes")
    def session_affinity_attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sessionAffinityAttributes"))

    @session_affinity_attributes.setter
    def session_affinity_attributes(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721291a5c6d5239247b9820181dc5aaa806e450bc620c284283bf729248bf051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinityAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityTtl")
    def session_affinity_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionAffinityTtl"))

    @session_affinity_ttl.setter
    def session_affinity_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7baa10ee941f7fac036d41647ca1bea605e34eae207a186012c3dd5e3d2142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinityTtl", value)

    @builtins.property
    @jsii.member(jsii_name="steeringPolicy")
    def steering_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "steeringPolicy"))

    @steering_policy.setter
    def steering_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4aac55686332dc3a0f2cab81ca46ae265a196d9b495e788347670f4b34d5bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "steeringPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba5df896ef2aab0c87f8466c80dd544574233b28e071a41e00576be3ecf36fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRulesOverrides, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRulesOverrides, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRulesOverrides, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978d57080a6f56d402e0e02c1bfbe681c0f68e6a9a73c1cf5ab8401ed2f86167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesPopPools",
    jsii_struct_bases=[],
    name_mapping={"pool_ids": "poolIds", "pop": "pop"},
)
class LoadBalancerRulesOverridesPopPools:
    def __init__(
        self,
        *,
        pool_ids: typing.Sequence[builtins.str],
        pop: builtins.str,
    ) -> None:
        '''
        :param pool_ids: See ```pool_ids`` <#pool_ids>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        :param pop: See ```pop`` <#pop>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop LoadBalancer#pop}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1598d7c3d8b093b6e3738f49f04782008a75b1f5ebb0708f6ddccd02f3302e5b)
            check_type(argname="argument pool_ids", value=pool_ids, expected_type=type_hints["pool_ids"])
            check_type(argname="argument pop", value=pop, expected_type=type_hints["pop"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_ids": pool_ids,
            "pop": pop,
        }

    @builtins.property
    def pool_ids(self) -> typing.List[builtins.str]:
        '''See ```pool_ids`` <#pool_ids>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        '''
        result = self._values.get("pool_ids")
        assert result is not None, "Required property 'pool_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def pop(self) -> builtins.str:
        '''See ```pop`` <#pop>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pop LoadBalancer#pop}
        '''
        result = self._values.get("pop")
        assert result is not None, "Required property 'pop' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRulesOverridesPopPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRulesOverridesPopPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesPopPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bc7dd8873c0059c41e4be5d50b4d758cbb8920096879002ed625c355d63789e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoadBalancerRulesOverridesPopPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a473b5b7f03abdda8a6bf03a69adf467a792c35cdf728c3310943bb423ccb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRulesOverridesPopPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee1bb36830286833fbea33d903a7430d80d249a2a2e95b26b98e0bde177c0d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84db5ab0f43bf23e23011f3bb232883cc8cdba85aebf3a207e8f4c6e708ef573)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cf77c4be80cf67871ab9e9eb190f757ca7f9f8e7517c395179407e98a74ad03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesPopPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesPopPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesPopPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625c3d994190bf96ccdbdc4449ff1de68726e68f289c1ec8e5af235a5538b62c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOverridesPopPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesPopPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__542d32c03ed609d9c7199a46b64dc04d9cc5de260bac18df45a13ce2f980d0b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="poolIdsInput")
    def pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "poolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="popInput")
    def pop_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "popInput"))

    @builtins.property
    @jsii.member(jsii_name="poolIds")
    def pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "poolIds"))

    @pool_ids.setter
    def pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3b6501787f99ce09f4ab99288f6b53bb1dbfc37473c9bdad1f6a086e750f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolIds", value)

    @builtins.property
    @jsii.member(jsii_name="pop")
    def pop(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pop"))

    @pop.setter
    def pop(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16358da404986b5fa2cd1304c03c95bd01214046adf6f1cf9a978743d3d8094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pop", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRulesOverridesPopPools, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRulesOverridesPopPools, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRulesOverridesPopPools, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fef62addfc7f7318117afbe793458f70fdf03332ef31dd2518087425719a712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesRandomSteering",
    jsii_struct_bases=[],
    name_mapping={"default_weight": "defaultWeight", "pool_weights": "poolWeights"},
)
class LoadBalancerRulesOverridesRandomSteering:
    def __init__(
        self,
        *,
        default_weight: typing.Optional[jsii.Number] = None,
        pool_weights: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
    ) -> None:
        '''
        :param default_weight: See ```default_weight`` <#default_weight>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_weight LoadBalancer#default_weight}
        :param pool_weights: See ```pool_weights`` <#pool_weights>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_weights LoadBalancer#pool_weights}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814c297157044678c5e2ceeefc86eb0d85f8b545d8d3ebf40f27a00b57851fa8)
            check_type(argname="argument default_weight", value=default_weight, expected_type=type_hints["default_weight"])
            check_type(argname="argument pool_weights", value=pool_weights, expected_type=type_hints["pool_weights"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_weight is not None:
            self._values["default_weight"] = default_weight
        if pool_weights is not None:
            self._values["pool_weights"] = pool_weights

    @builtins.property
    def default_weight(self) -> typing.Optional[jsii.Number]:
        '''See ```default_weight`` <#default_weight>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#default_weight LoadBalancer#default_weight}
        '''
        result = self._values.get("default_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pool_weights(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        '''See ```pool_weights`` <#pool_weights>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_weights LoadBalancer#pool_weights}
        '''
        result = self._values.get("pool_weights")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRulesOverridesRandomSteering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRulesOverridesRandomSteeringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesRandomSteeringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d38dbcaf3dd37de387d11aff964ae1a8d2db990c589565c723788a738252c3e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoadBalancerRulesOverridesRandomSteeringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7ee96db38b6baa8e94a8730b7b12d1e03019d3878e54ec4767cd053708102d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRulesOverridesRandomSteeringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf8e7a11515f0ca0559048e8d3dada2a18f5cd185f5e758160392cb70fc02d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef7734929423f89ed1430eea0015cb9d39bb8b1db1056b4b7af1f26d10ab3ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b500c72115a3887e5eb591d9c540756c7dc77f4f5593a945c2d8c31f440db878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesRandomSteering]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesRandomSteering]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesRandomSteering]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f6a41140f0c05763fa4a7d35cc3873b7ee65ce6f3d759313d9554f57a1769e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOverridesRandomSteeringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesRandomSteeringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5b2d542c2795328bfc394989129f5dbfdca043e9a83038e624a9420b89d61ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDefaultWeight")
    def reset_default_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultWeight", []))

    @jsii.member(jsii_name="resetPoolWeights")
    def reset_pool_weights(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPoolWeights", []))

    @builtins.property
    @jsii.member(jsii_name="defaultWeightInput")
    def default_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="poolWeightsInput")
    def pool_weights_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], jsii.get(self, "poolWeightsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultWeight")
    def default_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultWeight"))

    @default_weight.setter
    def default_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976e1879118b3b9cb7164040c9c8c6689e1fb358b87d54fe6ca924b8acbba5d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultWeight", value)

    @builtins.property
    @jsii.member(jsii_name="poolWeights")
    def pool_weights(self) -> typing.Mapping[builtins.str, jsii.Number]:
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "poolWeights"))

    @pool_weights.setter
    def pool_weights(self, value: typing.Mapping[builtins.str, jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abdee6acee4f1ad305fe73df9fed1e5c23781c31a2fb93c4affefd6f908beabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolWeights", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRulesOverridesRandomSteering, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRulesOverridesRandomSteering, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRulesOverridesRandomSteering, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eddaf802316fdf31096e07403abb5527856dd04d08509e317383300813b7b023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesRegionPools",
    jsii_struct_bases=[],
    name_mapping={"pool_ids": "poolIds", "region": "region"},
)
class LoadBalancerRulesOverridesRegionPools:
    def __init__(
        self,
        *,
        pool_ids: typing.Sequence[builtins.str],
        region: builtins.str,
    ) -> None:
        '''
        :param pool_ids: See ```pool_ids`` <#pool_ids>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        :param region: See ```region`` <#region>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region LoadBalancer#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7372a6c4bceaa2f6f8145dc6cf99c85cd93f20b594802d0671d5553db7f53c05)
            check_type(argname="argument pool_ids", value=pool_ids, expected_type=type_hints["pool_ids"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_ids": pool_ids,
            "region": region,
        }

    @builtins.property
    def pool_ids(self) -> typing.List[builtins.str]:
        '''See ```pool_ids`` <#pool_ids>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#pool_ids LoadBalancer#pool_ids}
        '''
        result = self._values.get("pool_ids")
        assert result is not None, "Required property 'pool_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def region(self) -> builtins.str:
        '''See ```region`` <#region>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer#region LoadBalancer#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerRulesOverridesRegionPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerRulesOverridesRegionPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesRegionPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64af56d636c0c9d3e3ad0eebc9c57d20f945402fed0d4a74a8069f7dd5097d71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoadBalancerRulesOverridesRegionPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3762ad1f839e20ec91c993ae680c999cf37c0ea12266a5a818d56f1a17248d05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerRulesOverridesRegionPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a754b8913bbda1f4757619f1c80963855c0ac9c3141f5d106c4650b58cb0195)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2308d720dbf45290f601a585ecb99097f84e25c4396ea87362a15ad2814b697f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8acd037a67816e7ab435b73974ffba9c7a1fe152023663be6bde4a8372da6985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesRegionPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesRegionPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesRegionPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43491ce5e11889cc24eb01f5d69bb3b720634c30d41b39341c893d27bbd7ab9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerRulesOverridesRegionPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancer.LoadBalancerRulesOverridesRegionPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f454c9c13e18cfe3b7a5d1fa443e6fc1bea5a0bdbca5965a6cdce9991ab42e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="poolIdsInput")
    def pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "poolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="poolIds")
    def pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "poolIds"))

    @pool_ids.setter
    def pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de75bccedc2e74222544c40134518d1ca4ba7014801d8bad7c955fc541aec17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolIds", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5df0fc1c80b9e5ea75329d48631e3a23ca4bec393d0986fc6e00724a83a0ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerRulesOverridesRegionPools, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerRulesOverridesRegionPools, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerRulesOverridesRegionPools, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a74337354c4c972dfbd70125096c0d8f0e658e058afaafa7a097fe6e4cfaa3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LoadBalancer",
    "LoadBalancerAdaptiveRouting",
    "LoadBalancerAdaptiveRoutingList",
    "LoadBalancerAdaptiveRoutingOutputReference",
    "LoadBalancerConfig",
    "LoadBalancerCountryPools",
    "LoadBalancerCountryPoolsList",
    "LoadBalancerCountryPoolsOutputReference",
    "LoadBalancerLocationStrategy",
    "LoadBalancerLocationStrategyList",
    "LoadBalancerLocationStrategyOutputReference",
    "LoadBalancerPopPools",
    "LoadBalancerPopPoolsList",
    "LoadBalancerPopPoolsOutputReference",
    "LoadBalancerRandomSteering",
    "LoadBalancerRandomSteeringList",
    "LoadBalancerRandomSteeringOutputReference",
    "LoadBalancerRegionPools",
    "LoadBalancerRegionPoolsList",
    "LoadBalancerRegionPoolsOutputReference",
    "LoadBalancerRules",
    "LoadBalancerRulesFixedResponse",
    "LoadBalancerRulesFixedResponseOutputReference",
    "LoadBalancerRulesList",
    "LoadBalancerRulesOutputReference",
    "LoadBalancerRulesOverrides",
    "LoadBalancerRulesOverridesAdaptiveRouting",
    "LoadBalancerRulesOverridesAdaptiveRoutingList",
    "LoadBalancerRulesOverridesAdaptiveRoutingOutputReference",
    "LoadBalancerRulesOverridesCountryPools",
    "LoadBalancerRulesOverridesCountryPoolsList",
    "LoadBalancerRulesOverridesCountryPoolsOutputReference",
    "LoadBalancerRulesOverridesList",
    "LoadBalancerRulesOverridesLocationStrategy",
    "LoadBalancerRulesOverridesLocationStrategyList",
    "LoadBalancerRulesOverridesLocationStrategyOutputReference",
    "LoadBalancerRulesOverridesOutputReference",
    "LoadBalancerRulesOverridesPopPools",
    "LoadBalancerRulesOverridesPopPoolsList",
    "LoadBalancerRulesOverridesPopPoolsOutputReference",
    "LoadBalancerRulesOverridesRandomSteering",
    "LoadBalancerRulesOverridesRandomSteeringList",
    "LoadBalancerRulesOverridesRandomSteeringOutputReference",
    "LoadBalancerRulesOverridesRegionPools",
    "LoadBalancerRulesOverridesRegionPoolsList",
    "LoadBalancerRulesOverridesRegionPoolsOutputReference",
]

publication.publish()

def _typecheckingstub__0015049507828df93e92dfe6c1bca8e51a3ffecfec278ed1f472e11b1c5ed18f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_pool_ids: typing.Sequence[builtins.str],
    fallback_pool_id: builtins.str,
    name: builtins.str,
    zone_id: builtins.str,
    adaptive_routing: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerAdaptiveRouting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    country_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerCountryPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    location_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerLocationStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pop_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPopPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    proxied: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    random_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRandomSteering, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRegionPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    session_affinity_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    session_affinity_ttl: typing.Optional[jsii.Number] = None,
    steering_policy: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__cd71b604d790772dd1e1e7eea42b70abcce9e3b559a9a9b30a69670c92ccbc65(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerAdaptiveRouting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50edfbde3fcf807556ccbf4a3c2735ad986bc9671861528170233fc398dacb9b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerCountryPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e05171f7beaedecec9431cd699717abfa6649fd62970384440f38de6f09e8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerLocationStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f2d23803906f9e0aa584834529e26d8492a405660336bfb106e903130394a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPopPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec78a491daf142014840778ab5eaf966681a5818db093b6dfa84b5b9fd485a55(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRandomSteering, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9adcb40f3b9090ef6dd1e7ceab37de12506e140f848103406a4e1e1b69039ed8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRegionPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713bf22a49b1560498a800316f840069503b2323554a05dc728d48b4c9dca764(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6089aef46269616117102dcd766828c839cd34a6ddc1a19b167be40df8a74eaf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749c6dd92b9de55f6f692a104109a7a8c0140668d57a671f2f4096578fa936a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c6dec4fe321e227c8d9680880282305431f4dba6c380b6d1257f0b33508764(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c848e190f535b767ecfa8d3c11f67ea8f02df867f678e83a7accbe2fcc7c48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee843cb964fbfddfe418aaaae462d730e400aab7fa1dc269ff018bb76f0398dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549a6fc7dd52b05e493a75e851006eb3ff4b1b5be4e31f42a3e0fba8a3e7992c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e098d3c0597e3524b55c3627f9a3bb7992a85e831d4f688b06dfff6966b3988(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0750582d833b47b92d0f19d520eb3c3efdee362ea8a4097af61978e00dce967a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd986c02bbc00cd38b69d6b9650c1f90ba2f88202d3989cddfc70f5f1707c0de(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0cd47fb3f2073bbd91e71dcb6d52e072ba67430ce8b3bd46319e7ae25f9afd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38cc45e4ba523e71f68dc6122fbd27e2295e3f03fc8776d0f26210fe4925bd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fcc62043aca63d073f33eb1730d5f1b0708a90f7fa61ae55fbbe0cebee22ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21bb86cc37c1ec4ce7603426eab2a13a53a3024685a2262c80dcf7351190a31b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303c8d660d7ff911b7607b1ed365324cf95aef52ab574f4228534f17fbfe1953(
    *,
    failover_across_pools: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90b6e6790528c206468d640490db3abef5a8c6eebaf718a4dd4418812b68081(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1559fb373ea400511817842976f6481ca4b702ec9d77caf629d01b47a72a6b80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72195fa870c62adbc2009d6ce6bcee0c275b9d355f65d6f5e8d9817c53c256db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83acfa63a7027123b02704d5e9a579ece4765d5ebc3c69f7ca90b31ac6ee89cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c506b6e06e7598e4219c30ddbe89a9325a76d05e43f16817b52d09bd0c01095(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3b4a1d4e77121ca9e6e6252584e0995b5d384fbc3f3c004f6c162fdc221751(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerAdaptiveRouting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41d79f69f4c4baa892cc9881ebe8a3b44e49a9e164ded9e679d66e3b05302c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483f29751055bdcab9b5325a954524c06820b6aca2f5bdcef6272c6c5e8f633d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4657374ad9caf633eb09b1d65ba4e5b4f17d06e0b28714a28b13cdc210bd62a(
    value: typing.Optional[typing.Union[LoadBalancerAdaptiveRouting, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179a274ba88b1187743571bdcd7d729435f5abbf8faf21f1b93231a9af798a1f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_pool_ids: typing.Sequence[builtins.str],
    fallback_pool_id: builtins.str,
    name: builtins.str,
    zone_id: builtins.str,
    adaptive_routing: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerAdaptiveRouting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    country_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerCountryPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    location_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerLocationStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pop_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPopPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    proxied: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    random_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRandomSteering, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRegionPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    session_affinity_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    session_affinity_ttl: typing.Optional[jsii.Number] = None,
    steering_policy: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b0daf3d0d177f60400d4a93728ab851bf10622630f28d737aeb8d7c2eee5a7(
    *,
    country: builtins.str,
    pool_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5548baca517597e80277b08da446c45a8f51631c8e33ff5c8752d5cd3a72440(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee511752c059d5fe31e6576972c7845577edf5266b0034f168b3800e3f8fbd01(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a03adce2efde6f1f00645b6dfcafff0849b9d18ab7b3cab77e5e682f4005551(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efbe75a11a9650fc79b6553f2273f5c605c08530aeb9cef5a87d1f174689749(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563a476817276bd3c54a24c10e0156f07d9ce998eca4226121fd1890142b75f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35965adf8611b7414765ef01ccff4401c14e6a1c5709fed9b03a5f5b2fa5365f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerCountryPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdc22231cdd036c54071ec37bf2a65a304f331e649108c1d23d78131b909f14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4ffc12370605081eaf6cca687742727921c5bb1c257d0e045a165a3e0dcf61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9973ba5fda63b86e30deb7aa8265935a5e08056740c2ac107f00efbb33752d90(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01fac163181d041e619ec731cf4eb19f20c5da329298ce5b7c00a06db152ef3(
    value: typing.Optional[typing.Union[LoadBalancerCountryPools, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d0457eea690b702cd82d00d1d62a0d5a8fe1280f78f5baff5cd4e5a844b3b2(
    *,
    mode: typing.Optional[builtins.str] = None,
    prefer_ecs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3636585e1fd34e70e4640cd6d7be47fd35ff440924016bed9fe10c92d51b817(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91a1e6cdd56a1366dd6120a236bb6b6b78dc2c088b14857cb5f1c5034f8e465(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88f05649b0e15c18d251c96b4d0b365a9e157c8e4d3be62a9f5f18dacfa3a6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c7b8f18e11daf0cd7927acb2bcf22cff2577b5dbb7bac45a97e2399e468b9b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac9c9a67ee7c88a21e0c107afd4b4a638fba43e06115f10e283c979c4381dbc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d540ff6c8ed8b8c2ea94bf4fe4b715599536ec4fe37e00eefc7bf0e2401fd7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerLocationStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81b5884646eb683c1088e82b1ba373165f971f9550ab7a9950624c0fa774f6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283834d4efe18f2ecca14babcc0cff3cc686560412d787bb702fb0f888ee83e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7502d6738609e16ad083c65590cb0aae8820f91260ffc08dc679caa3a79d05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154dac22f09bd45bd574fb93d3a050a49415bdd268301d55ed3771479657a7a2(
    value: typing.Optional[typing.Union[LoadBalancerLocationStrategy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33959bd2b04d58ab97c408caf9651653bfa0be987b6eab3c6d4421d0fae7f16b(
    *,
    pool_ids: typing.Sequence[builtins.str],
    pop: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f89461863299705db1cba4af17061563d33fa656949aac3d70cee1aee04907(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eed29d5ce9b0e646119d2e53c5d8122e9118aa76be22a1b2925e3452f9dd2ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd5176f46154ebbc237ceec96c7d6ed2e3a76b54c718b6a738a8e68080c6e80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddeb513de7b059571c8bd61ba7c4b4922f85ff1f7f7d3291be043ddc56bbf91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b27c390956528201cd3f387829ec0a2eb4613290f074be0d213875f77e8f1cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5959a17b4c9e55b6dbdf79ee4a421978077f003a69dc25996b54cd9010d0b7f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPopPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84781d122a88e5c575953503e586a779f2a1548efff52d90cf2e043733f8ee4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208ab23cda9b812c72e86ae04ee2ce9ce7a25fbfab670853bddc25cc2da49031(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d031cac610c522a5f74485725bcc2f4f29fef327e00a75a8c27eaa604b1f0134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672260e434f5c32d7753e04817acb246b7c4d746aaf1c7b5d96f07e0378361c6(
    value: typing.Optional[typing.Union[LoadBalancerPopPools, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee03b4afc82f161efabb876910cdab21e26982c73d8eef161bdf1806f028519b(
    *,
    default_weight: typing.Optional[jsii.Number] = None,
    pool_weights: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632645b91a77660587cbc1ba26291b0820892ad8d8dbc3908e74e4b5d1bc6a33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49754c2b67088eb68cf724681fa4f887bfc9718dec179e0c0717c8606db04d19(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e60d66fc66b196b3d04a3274188d99a230d055956f2146b5dba2b3edebc57f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be22d3daddfdb6dabb2258f4252ae26ba0c8f73f9df7b460a2fc1087dc2d60b8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e7502eed605864fe5c76fa994a54205d98b918c73fdf639a34f00ee468be6a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5790f54b965a1b90119a410dcd2a92db95e4b443668c1955188310c5e89b50b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRandomSteering]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eff3856a00584fdf493670649b9ffda272af232d2ba2774e2a2317ee7892ea4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64146deae2c3ed36b3305117fa981b5b7c9a1164677f036cb508f162493c0086(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9973a0c91cce2364e7bca20eead582d2bb02780a7f8a4182cefbd38c49d0b90(
    value: typing.Mapping[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecaf7995fee6243343cf4dfffae58904bdf43c75cc42227c30cfacfa4083ed8(
    value: typing.Optional[typing.Union[LoadBalancerRandomSteering, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c8d4144cb636bf8b01cfe1d17204a0016b1c54e821d1f4c5b79a10641db53e(
    *,
    pool_ids: typing.Sequence[builtins.str],
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e6663dfe2a4a8c169517bbd45c29fc6c961e6d87abdb4f554e078842efec25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1b1d353584d0e935cad04a58df6efe2914c1184a0672c1855bcaa81df914f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aed4140b729002e0421cc7fd26ac7935f4eff3666b8879b389b3d4812899a15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a562f6de04282898ce16a3544850b17d09b0a70b13f9dfc8fc0e4ddfe1f9c2aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb91ea7c56abd8721824126b4b32b96e04867762adffd58552d4ba63d522050b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d086972694af7ebbf3146f856de93494d223c98382d014300f4d0779172131(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRegionPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61aa2c8772eb177ee7c1aeeb0e613107818a4c08aeecc835d33f3b759978751(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ed2ab576dea8049ab36066f6772645f3f6529e8316e192ed60fbd31efd8b48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e4773fde1a9c08d688e3199f0a5242863d3965d7005829cbb249f47f053c9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dbf6c2b118bdc11525d869dfec93cdf977ff48aa452e66e94599e2bb880e5a(
    value: typing.Optional[typing.Union[LoadBalancerRegionPools, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fdf42061a6652ffd6986a8e2ec9edad4427316f2d7a2321fe44f8214e666716(
    *,
    name: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fixed_response: typing.Optional[typing.Union[LoadBalancerRulesFixedResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    terminates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06a358aa30363c798305232d6e623350e1f1c44109315e688dbf167c0529967(
    *,
    content_type: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    message_body: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80108d9aa8c23f36e4b7063ba0aa4b31c3e1275949022514800f4c8eb0d14916(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86270d9848d23db8e4200b0e35ebc9fc45e5da1d517d6a31bc7780f890383a91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b015c6e42a266873f9a700c8a31631697378013d1c81a51f6dee7696471a23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69434f811e173e46da313f9aedd1026400d0a3b9a0174f3f0300bfbc6774e9f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf77b24367c791875e918c3a9cedf3f2147f45e4dacbb0aeb750962fad39bd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1307772712904f3a25b1d8ff5167a3a18cacea694ac2ce73bd9c48607726e4a(
    value: typing.Optional[LoadBalancerRulesFixedResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59baa239d8e3ea247aac1525b719e2de365c0547c13a6e6738e91104b679e18f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd5d663b462645948272bde24a3e6a192a833e4d72fadcfbe9d26e8affa9a19(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd04c38c24c581759071ae44418fc173fd284b9cd0edbbd2f85e435c9c1c578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521357c4039603ba4551315908639be87cc4d2d45ba7c9ab2982e88e9e19fe09(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db24e37e9660436ce55e2591e403ae318662c1893aea722586425995eeb689f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2aab7db6cb77dc7546b011c288f299e644f90b4e6681a5fadb150655069bd9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb822e0195a87da51205f90f18bdae2e8a011b0c0b8be0a23f2767a53a54c34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1128822e7fffe327616b8160ad4df31c1407481a501f919f59f92034cee83171(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc94eb429048c5fdcba032f9097bff452e96a8b87a21ed14207910ff9ebd8e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970524bed5e99690908d85d4d7ac78a7ba44a085d24880cb72687193e0e9bc09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7098ca56037e693d628373e3a6f18993274641304d612d1ad77069af9d82e1ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3294de3d4a5c794f3bceef16b338e69245d8e1474e2ca04d3e6c6914850bd6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66223bd8cfe2d18c3c9439fce67488c94926fc3e7f8f4f9a245979aa2a5bdce8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be777163ff6c1b6b7d0e9fbbc7f8a8d9c7d76e6976ca4eeac1712b453685526(
    value: typing.Optional[typing.Union[LoadBalancerRules, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f9ec836d04efd6df32310c87de2c9677c1832a61280179f4a5f5628a3a2bdc(
    *,
    adaptive_routing: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesAdaptiveRouting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    country_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesCountryPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    fallback_pool: typing.Optional[builtins.str] = None,
    location_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesLocationStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pop_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesPopPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    random_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesRandomSteering, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesRegionPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    session_affinity_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    session_affinity_ttl: typing.Optional[jsii.Number] = None,
    steering_policy: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e2e8cb8e4a79360b5de5e2325232e4c6100f6a32a2ab352bcb66c2d74ad625(
    *,
    failover_across_pools: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8b3e5b80047cb5c9976482c22083a7597952c88d6940a50955f79e33844b48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570bc537028c697b0d4d1377f495366a2c4317e9105e963853a68b707b4629dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df15b04ba4fc8c8cc34c3e3f41374780eeb0c45877d65c567120155c3fd8ebd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bbd90daa4fdd900e3fdff88bbfc460f38e4a288a2b7629a481ac391b89381f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6667d3650106a5eaeca757c9e1f029bd6f17994ed158e101a290c18ed2eb8ca5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2747a5877a5ba632852ba597a7c003924ec2855f4b0f20981ddb4f8588893050(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesAdaptiveRouting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7efd7e78658287b28e5ba6c9d99fd5f22803fb81fd0c9a750d67e5c32faa5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba808bf362e4eba92256ff998ed3db7c2a9341a8469fb85e0563777f8442a0f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacd7002058763798e137aaa37b1041267fb13953033e1caaf6edee7a3356bc0(
    value: typing.Optional[typing.Union[LoadBalancerRulesOverridesAdaptiveRouting, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd268733c4bc495a9fc0207b00546529b5588c4377ee5d92d1460d51d8aca7a8(
    *,
    country: builtins.str,
    pool_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68f1ce3ce85a721c6987514ea6f744969031db22026dcba02cf404e7a57f320(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52610fc2d63e239a20114270ede8042b2be3c39e7506d36782c9d5f808c5f359(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ccd859b55a9e20f703ff1f1605dfaa1bc099b8d4c303efe0dfa47461e1b2478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb389ca7c85f896b516017288618048963ebbf4d5abe8c69c0b45fd04ad0410(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b6517e781dbd2d2c0e11fd980c17688bd45e4422a433b40e74c4c395f3ada1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64b0a55f0a7c206e1f2a0ebf5e7fa3c88c08fc5c1f1a7f45f2160841e5fd776(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesCountryPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af5414311dbda1ee3a2f6f5e125a1421117934b111d152fabcad27eb8f936b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a2867eb44234989b462c76861e6e3b7197c18f84e2c0e4f08137f20a7a7227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e663f2de378a95564859a1574956f2326064841d42b13aa3d78dcbb26ddf0bd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e3f7bf2f9e3bdb8cc5e57d5fc525d0ecc208ebfa5bac859004c59e8a1f981c(
    value: typing.Optional[typing.Union[LoadBalancerRulesOverridesCountryPools, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fe80b59272da0ca21b3486df6e040943336c01fc85eb15870b312b293fe8aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d90b4c69a4eda8f37e43836fa234cbe4c1624bef4d909dbffb193e52186af67(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7adfb9f90bd97359ccd54defbd20e2f75fbb0d8c4e8ed595d8a7ffd1b67ca1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b6e6fe9ee2f96215beef92deb67164a373407cc3674f438ec297a7ff9881ab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2f5819aae0177d2bbeac41763bfb844aedce6524d21217dcbb672200bcecb1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7619d73070d4f912d64e6909f2709aa21c67ecc5c86eae5592d9f048ff0dc67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7071e21700e31fa074b8b5a8eaf06b619702a637def0209b2bdd1687d7355b4d(
    *,
    mode: typing.Optional[builtins.str] = None,
    prefer_ecs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e88c5a0246cca43aa487213704888993206b309da6e67f41418d6035746998(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fc10eeb62aac0ce3f9fb31b3fc779a921cf7411cb8c77b8f9bdb3603fe0215(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53eb57e34490025a67c8a9373fb209a9df76a132f2d7be2f100a68245c8d7f0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b65ae2a0783d3cade92ed09359597e8e0a8c04afc44ec2bc144b5108c8c10e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ebb525e7fa445afd391826eee32224f7aa03721b387679d473f06cef1dc94f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825eeb81e2bc1b86f9b554bff0d78c03113e4146bb55ee6fdbaf83c5b0a54ddb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesLocationStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a0b307a30466237be574a87cdd5702cd9422a2a7e41360c7c9d139a12a13e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13fca12df2c10577502f0351db487d810d4b94dc8597c923a699d999c6fd7a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7707eb1046a2a52ab76b39bfc611852997beee3f5cdb6c4daaa504f72a21bb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41515753604db88b8a568c09f635d7871ab23948ab008963bb5bd6b91a07c93(
    value: typing.Optional[typing.Union[LoadBalancerRulesOverridesLocationStrategy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e3db2746899b32772fe9f12603f7f273304443e2cde098ff2fb855c3740b76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9708d8bd193f530f009e042f15882c02f8056700b0642dd2abefd700d12e61(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesAdaptiveRouting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c0ffa07868d796a1d914c5ed8b779cabfde4d7f527fbf0efbdacd9e3a88ed7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesCountryPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831f41ebcc9b91a9de41e35f12b1c897ad9cc07c119ff11f950d724081314481(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesLocationStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ffddd4d0e832c5b8e2916c3fca7480aa774d9519356bc045263f4e10269f0e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesPopPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4882363e961f3c6242cbee0b4644c626fe313c4a1d0e9e154661d63345fa08b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesRandomSteering, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bab50d248c46cc9750589d219f3f105eda534c26bebd16f774ff2fcf46597c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerRulesOverridesRegionPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b23a730bb6221ed135022ddefe56c86eb339adfcc39f52819954e7fa4ab46b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87420889d83d51684a80a5b6b9732740355fca6a277bd0004154f57e679dfab0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2135424592a76b8f56aebfbdbd15a33640fb261375c502e64873fae4cbbb98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721291a5c6d5239247b9820181dc5aaa806e450bc620c284283bf729248bf051(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7baa10ee941f7fac036d41647ca1bea605e34eae207a186012c3dd5e3d2142(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4aac55686332dc3a0f2cab81ca46ae265a196d9b495e788347670f4b34d5bcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba5df896ef2aab0c87f8466c80dd544574233b28e071a41e00576be3ecf36fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978d57080a6f56d402e0e02c1bfbe681c0f68e6a9a73c1cf5ab8401ed2f86167(
    value: typing.Optional[typing.Union[LoadBalancerRulesOverrides, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1598d7c3d8b093b6e3738f49f04782008a75b1f5ebb0708f6ddccd02f3302e5b(
    *,
    pool_ids: typing.Sequence[builtins.str],
    pop: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc7dd8873c0059c41e4be5d50b4d758cbb8920096879002ed625c355d63789e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a473b5b7f03abdda8a6bf03a69adf467a792c35cdf728c3310943bb423ccb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee1bb36830286833fbea33d903a7430d80d249a2a2e95b26b98e0bde177c0d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84db5ab0f43bf23e23011f3bb232883cc8cdba85aebf3a207e8f4c6e708ef573(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf77c4be80cf67871ab9e9eb190f757ca7f9f8e7517c395179407e98a74ad03(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625c3d994190bf96ccdbdc4449ff1de68726e68f289c1ec8e5af235a5538b62c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesPopPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542d32c03ed609d9c7199a46b64dc04d9cc5de260bac18df45a13ce2f980d0b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3b6501787f99ce09f4ab99288f6b53bb1dbfc37473c9bdad1f6a086e750f56(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16358da404986b5fa2cd1304c03c95bd01214046adf6f1cf9a978743d3d8094(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fef62addfc7f7318117afbe793458f70fdf03332ef31dd2518087425719a712(
    value: typing.Optional[typing.Union[LoadBalancerRulesOverridesPopPools, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814c297157044678c5e2ceeefc86eb0d85f8b545d8d3ebf40f27a00b57851fa8(
    *,
    default_weight: typing.Optional[jsii.Number] = None,
    pool_weights: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38dbcaf3dd37de387d11aff964ae1a8d2db990c589565c723788a738252c3e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7ee96db38b6baa8e94a8730b7b12d1e03019d3878e54ec4767cd053708102d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf8e7a11515f0ca0559048e8d3dada2a18f5cd185f5e758160392cb70fc02d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef7734929423f89ed1430eea0015cb9d39bb8b1db1056b4b7af1f26d10ab3ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b500c72115a3887e5eb591d9c540756c7dc77f4f5593a945c2d8c31f440db878(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f6a41140f0c05763fa4a7d35cc3873b7ee65ce6f3d759313d9554f57a1769e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesRandomSteering]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b2d542c2795328bfc394989129f5dbfdca043e9a83038e624a9420b89d61ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976e1879118b3b9cb7164040c9c8c6689e1fb358b87d54fe6ca924b8acbba5d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abdee6acee4f1ad305fe73df9fed1e5c23781c31a2fb93c4affefd6f908beabf(
    value: typing.Mapping[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddaf802316fdf31096e07403abb5527856dd04d08509e317383300813b7b023(
    value: typing.Optional[typing.Union[LoadBalancerRulesOverridesRandomSteering, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7372a6c4bceaa2f6f8145dc6cf99c85cd93f20b594802d0671d5553db7f53c05(
    *,
    pool_ids: typing.Sequence[builtins.str],
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64af56d636c0c9d3e3ad0eebc9c57d20f945402fed0d4a74a8069f7dd5097d71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3762ad1f839e20ec91c993ae680c999cf37c0ea12266a5a818d56f1a17248d05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a754b8913bbda1f4757619f1c80963855c0ac9c3141f5d106c4650b58cb0195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2308d720dbf45290f601a585ecb99097f84e25c4396ea87362a15ad2814b697f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8acd037a67816e7ab435b73974ffba9c7a1fe152023663be6bde4a8372da6985(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43491ce5e11889cc24eb01f5d69bb3b720634c30d41b39341c893d27bbd7ab9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerRulesOverridesRegionPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f454c9c13e18cfe3b7a5d1fa443e6fc1bea5a0bdbca5965a6cdce9991ab42e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de75bccedc2e74222544c40134518d1ca4ba7014801d8bad7c955fc541aec17c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5df0fc1c80b9e5ea75329d48631e3a23ca4bec393d0986fc6e00724a83a0ced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a74337354c4c972dfbd70125096c0d8f0e658e058afaafa7a097fe6e4cfaa3d(
    value: typing.Optional[typing.Union[LoadBalancerRulesOverridesRegionPools, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
